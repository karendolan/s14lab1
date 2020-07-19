/**
 * @class Bars
 */
class Bars {

   // Variables
   data_bins = [];

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
    histogram = d3.histogram();
    scX = d3.scaleLinear()
            .range([0, this.gW]);
    scY = d3.scaleLinear()
            .range([this.gH, 0]);
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
            .text('Age');
        vis.yAxisG = vis.g.append('g')
            .attr('class', 'axis axisY')
            .style('transform', `translateX(${-15}px)`);
        vis.yAxisG.append('text')
            .attr('class', 'label labelY')
            .style('transform', `rotate(-90deg) translate(-${vis.gH / 2}px, -30px)`)
            .text('Totals');
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

        // Map ages
        const ageMap = vis.data.map(d => d.age);
        // console.log('ageMap', ageMap);

        // HIstograph
        vis.data_bins = vis.histogram(ageMap);
        // console.log("Bins " + vis.data_bins);

        // Update scales
        vis.scX.domain(d3.extent(ageMap,d => d));
        vis.scY.domain([0, d3.max(vis.data_bins,d => d.length)]);
        vis.xAxis.scale(vis.scX).ticks(vis.data_bins.length);
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
         vis.g.selectAll('.barG')
             .data(vis.data_bins)
             .join(
                 enter => enter
                     .append('g')
                     .attr('class', 'barG')
                     .each(function(d, i) {
                         // Define this
                         const g = d3.select(this);

                         // Get dims
                         const w = Math.round(vis.gW / vis.data_bins.length);
                         const h = vis.scY(d.length);

                         // Position
                         g.style('transform', `translate(${w * i}px, ${h}px)`);

                         // Append rect
                         g.append('rect')
                             .attr('width', Math.floor(w * 0.8))
                             .attr('height', vis.gH - h)
                             .attr('x', Math.floor(w * 0.1))
                             .attr('fill', 'rgba(0, 0, 255, 1)');

                     })
             );

         // Update axis
         vis.xAxisG.call(vis.xAxis);
         vis.yAxisG.call(vis.yAxis);

     }
 }
