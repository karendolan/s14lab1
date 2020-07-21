/**
 * @class Donut
 *
 * A donut chart that represents the different programing languages,
 * and shows the results in the center when hovering.
 *
 *
 *
 */
class Donut {

    // Variables
    data_bins = [];

    // Elements
    svg = null;
    g = null;

    // Configs
    svgW = 320;
    svgH = 320;
    svgM = 50;
    gMargin = {top: 20, right: 20, bottom: 20, left: 20};
    gW = this.svgW - (this.gMargin.right + this.gMargin.left);
    gH = this.svgH - (this.gMargin.top + this.gMargin.bottom);
    radius = Math.min(this.svgW, this.svgH) / 2 - this.svgM;

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
            .style('transform', `translate(${vis.svgW/2}px , ${vis.svgH/2}px)`);

        // Append Header label
        vis.xTextLabelg = vis.g.append('g')
            .attr('class', 'axis axisX');
        vis.xTextLabelg.append('text')
            .attr('class', 'label labelX')
            .style('transform', `translate(0,-${vis.radius + 10}px)`)
            .text('Programing Languages');

        // Path hover text information
        vis.xTextInfog = vis.g.append('g')
            .attr('class', 'infoText')
            .style('transform', `translate(-20px,0)`);
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

        // Map programing languages
        let progLangMap = {};
        vis.data.forEach(d => {
          progLangMap[d.prog_lang] = (progLangMap[d.prog_lang] || 0) + 1;
        });
        //console.log('progLangMap', progLangMap);
        const progLangArray = Object.keys(progLangMap).map((key) => {
          return {
            'count' : progLangMap[key],
            'name' : key
          };
        });
        //console.log('progLangArray', progLangArray);

        // Set the arcs
        vis.data_bins = d3.pie()
          .value(d => d.count)(progLangArray);
        //console.log('data_bins', vis.data_bins);

        // Generate the arc
        vis.arc = d3.arc()
            .innerRadius(vis.radius / 2)
            .outerRadius(vis.radius);

        // Set the color scale
        // From https://www.d3-graph-gallery.com/graph/donut_basic.html
        // Random color generator
        // From https://stackoverflow.com/questions/1484506/random-color-generator
        vis.color = d3.scaleOrdinal()
          .domain(vis.data_bins.map(d => d.data.name))
          .range(vis.data_bins.map(() => {
             return '#'+Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
          }));

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

        // [Time to] make the donut
        vis.g.selectAll('.arc')
            .data(vis.data_bins)
            .enter()
            .append("path")
            .attr('class', 'arc')
            .attr("d", vis.arc)
            .attr("fill", d => vis.color(d.data.name))
            .attr("stroke", "gray")
            .attr("stroke-width", 1)
            .on('mouseover', d => {
              vis.xTextInfo.text(`${d.data.name} (${d.data.count})`);
            });

    }
}
