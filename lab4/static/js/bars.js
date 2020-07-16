/**
 * @class Bars
 */
class Bars {

   // Variables
   data_bins = [];

    // Elements
    svg = null;
    g = null;

    // Configs
    svgW = 360; // in px
    svgH = 360;
    gMargin = {top: 0, right: 0, bottom: 0, left: 0};
    gW = this.svgW - (this.gMargin.right + this.gMargin.left);
    gH = this.svgH - (this.gMargin.top + this.gMargin.bottom);

    // Tools
    histogram = d3.histogram;
    scX = d3.scaleLinear()
        .range([0, this.gW]);
    scY = d3.scaleLinear()
        .range([0, this.gH]);

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
        console.log("Bins " + vis.data_bins);

        // Update scales
        vis.scX.domain(d3.extent(ageMap, d=> d));
        // console.log("Bins 1 " + vis.scX.range() + '/' + vis.scX.domain());
        vis.scY.domain([0, d3.max(vis.data_bins, d=> {
          d.length
        })]);
        // console.log("Bins 2 " + vis.scY.range() + '/' + vis.scY.domain());

        // Now render
        vis.render();
    }

    /** @function wrangle()
     * Builds, updates, removes elements in vis
     *
     * @returns void
     */
    render() {
        // Define this vis
        const vis = this;

        // Create Bars / bind data
        const showMe = vis.g.selectAll('.barG')
            .data(vis.data_bins)
            .join(
              // Enter  - adding new elements/data
              enter => enter
                .append('g')
                .attr('class', 'barG')
                .each(function(d, i) {
                  console.log(this);

                  const g =  d3.select(this);
                  const w = Math.round(x:vis.gW/vis.data_bins.length);

                  //Position
                  g.style('transform', `transform(${w * i}px)`);
                  g.append('rect')
                   .attr('width', vis.gW / vis.data_bins)
                   .attr(name: 'height', vis.scY(d.length))
                })
            );
        console.log("showMe");
        console.log(showMe);

    }
}
