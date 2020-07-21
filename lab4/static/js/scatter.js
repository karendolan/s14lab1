/**
 * @class Scatter
 */
class Scatter {

   // Variables
   data_bin = [];

    // Elements
    svg = null;
    g = null;
    xAxisG = null;
    yAxisG = null;

    // Configs
    svgW = 360; // in px
    svgH = 360;
    gMargin = {top: 50, right: 50, bottom: 60, left: 80};
    gW = this.svgW - (this.gMargin.right + this.gMargin.left);
    gH = this.svgH - (this.gMargin.top + this.gMargin.bottom);

    // Tools
    scX = d3.scaleLinear()
            .range([0, this.gW]);
    scY = d3.scaleLinear()
            .range([this.gH, 0]);
    scR = d3.scaleSqrt()
             .range([1.5, 3]);
    xAxis = d3.axisBottom();
    yAxis = d3.axisLeft().ticks(5);


    /*
    Constructor
     */
    constructor(_data, _target) {
        // Assign parameters as object fields
        this.data = _data;
        this.target = _target;

        // Now init
        this.init();
    }

    /** @function init()
     * Perform one-time setup function
     *
     * @returns void
     */
    init() {
        // Define this vis
        const vis = this;

        // Set up the svg/g work space
        vis.svg = d3.select(`#${vis.target}`)
            .append('svg')
            .attr('width', vis.svgW)
            .attr('height', vis.svgH);
        vis.g = vis.svg.append('g')
            .attr('class', 'container')
            .style('transform', `translate(${vis.gMargin.left}px, ${vis.gMargin.top}px)`);

        // Append axes
        vis.xAxisG = vis.g.append('g')
            .attr('class', 'axis axisX')
            .style('transform', `translateY(${vis.gH + 15}px)`);
        vis.xAxisG.append('text')
            .attr('class', 'label labelX')
            .style('transform', `translate(${vis.gW / 2}px, 40px)`)
            .text('Years of Experience');
        vis.yAxisG = vis.g.append('g')
            .attr('class', 'axis axisY')
            .style('transform', `translateX(${-15}px)`);
        vis.yAxisG.append('text')
            .attr('class', 'label labelY')
            .style('transform', `rotate(-90deg) translate(-${vis.gH / 2}px, -30px)`)
            .text('Homework Hours');

        // Path hover text information
        vis.xTextInfog = vis.g.append('g')
            .attr('class', 'infoText')
            .style('transform', `translate(20px,0)`);
        vis.xTextInfo = vis.xTextInfog.append('text')
            .attr('class', 'info infoX')
            .text('');  //this is set on donut secgtion hover

        // Now wrangle
        vis.wrangle();
    }

    /** @function wrangle()
     * Preps data for vis
     *
     * @returns void
     */
    wrangle() {
        // Define this vis
        const vis = this;
        // console.log('Data', vis.data);

        // "experience_yr": 7.0,
        // "hw1_hrs": 5.0,
        // Map years to hours
        let yearsExpMap = [];
        vis.data_bin = vis.data.map(d => {
          return {
            yrsExp : d.experience_yr,
            hwHrs : d.hw1_hrs,
            age : d.age
          }
        });
        // console.log('data bin', vis.data_bin);

        // Update scales
        vis.scX.domain(d3.extent(vis.data_bin,d => d.yrsExp));
        vis.scY.domain([0, d3.max(vis.data_bin,d => d.hwHrs)]);
        // Using Age for dot size scaler
        vis.scR.domain(d3.extent(vis.data_bin,d => d.age));

        vis.xAxis.scale(vis.scX);
        vis.yAxis.scale(vis.scY);

        // Now render
        vis.render();
    }

    /** @function render()
     * Builds, updates, removes elements in vis
     *
     * @returns void
     */
     render() {
         // Define this vis
         const vis = this;

         // Build bars
         const dots = vis.g.selectAll('.dot')
             .data(vis.data_bin)
             .join(
                 enter => enter
                     .append('g')
                     .attr('class', 'dot')
                     .each(function(d, i) {
                         // Define this
                         const g = d3.select(this);

                         // Position
                         const x = vis.scX(d.yrsExp);
                         const y = vis.scY(d.hwHrs);
                         // Position
                         g.style('transform', `translate(${x}px, ${y}px)`);
                         //console.log(x +" "+ y);

                         // Append rect
                         g.append('circle')
                             .attr("r", vis.scR(d.age))
                             .attr('fill', 'rgba(0, 0, 255, 1)')
                             .attr('class', 'dot-circle')
                             .on('mouseover', d => {
                               vis.xTextInfo.text(`Age ${d.age}`);
                               vis.xTextInfog.style('transform', `translate(${x}px, ${y}px)`);
                             })
                       })
              );

         // Update axis
         vis.xAxisG.call(vis.xAxis);
         vis.yAxisG.call(vis.yAxis);

     }
 }
