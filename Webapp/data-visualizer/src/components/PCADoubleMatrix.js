import react, {Component, lazy} from 'react';
import {studies, formatStudyName} from '../Datasets';
//import PCA from 'pca-js';
import Plot from 'react-plotly.js';
//import * as d3 from 'd3';
import meta from '../data/PCADouble/meta.json';
import {RightMenuContainer, RightMenuCheckbox, RightMenuSelector, RightMenuNumberInput, RightMenuMultiselect} from './RightMenu';

class Selection extends Component {
    render() {
        return (
            <RightMenuContainer>
                <RightMenuMultiselect label="Datasets x-axis" value={this.props.studies1} onChange={this.props.changeStudies1}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                 <RightMenuMultiselect label="Datasets y-axis" value={this.props.studies2} onChange={this.props.changeStudies2}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                 <RightMenuSelector label="PCA based on" value={this.props.pcaBase} onChange={this.props.changePCABase}
                    optionValues={["x-axis", "y-axis", "joint"]}
                    optionNames={["X-axis dataset", "Y-axis dataset", "Both"]} />
                <RightMenuSelector label="PC x-axis" value={this.props.pc1} onChange={this.props.changePC1}
                    optionValues={[...Array(10)].map((_, i) => i)}
                    optionNames={[...Array(10)].map((_, i) => i + 1)}
                    optionDisabled={[...Array(10)].map((_, i) => this.props.pc2 == i)}
                    oneLine={true}
                    />
                <RightMenuSelector label="PC y-axis" value={this.props.pc2} onChange={this.props.changePC2}
                    optionValues={[...Array(10)].map((_, i) => i)}
                    optionNames={[...Array(10)].map((_, i) => i + 1)}
                    optionDisabled={[...Array(10)].map((_, i) => this.props.pc1 == i)}
                    oneLine={true}
                    />
                <RightMenuNumberInput label="Marker size" min="1" max="20" value={this.props.markerSize} 
                    onChange={this.props.changeMarkerSize} oneLine={true}/>
                <RightMenuNumberInput label="Opacity" min="0" max="1" step="0.05" value={this.props.opacity} 
                    onChange={this.props.changeOpacity} oneLine={true}/>
                <RightMenuCheckbox label="Separate case and controls" checked={this.props.separateCaseControl}
                    onChange={this.props.changeSeparateCaseControl}/>
            </RightMenuContainer>
        )
    }
}

class PCADoubleMatrixPlot extends Component{

    constructor(props){
        super(props);
        this.state = {height: window.innerHeight};
        this._isMounted = false;
    }
    
    updateSize(){
        this.setState({height: window.innerHeight});
    }

    componentWillUnmount(){
        this._isMounted = false;
        window.removeEventListener("resize", this.updateSize.bind(this));
    }

    componentDidMount(){
        this._isMounted = true;
        window.addEventListener("resize", this.updateSize.bind(this));
        for (const study1 of this.props.studies1) {
            for (const study2 of this.props.studies2) {
                if (study1 !== study2 && meta[study1][study2]["joint"] > Math.max(this.props.pc1, this.props.pc2)) {
                    fetch(`/data/PCADouble/${study1}_vs_${study2}.json`).then(r => r.json()).then(data => {
                        data = data[{
                            "x-axis": study1,
                            "y-axis": study2,
                            "joint": "joint"
                        }[this.props.pcaBase]];
                        const transformed = {};
                        [study1, study2].forEach(s => {
                            transformed[s] = {};
                            transformed[s]["both"] = [data[s][this.props.pc1], data[s][this.props.pc2]];
                            transformed[s]["cases"] = [data[s][this.props.pc1].filter((_, ind) => data[s]["cancer"][ind]),
                            data[s][this.props.pc2].filter((_, ind) => data[s]["cancer"][ind])];
                            transformed[s]["controls"] = [data[s][this.props.pc1].filter((_, ind) => !data[s]["cancer"][ind]),
                            data[s][this.props.pc2].filter((_, ind) => !data[s]["cancer"][ind])];
                        });
                        const s = {};
                        s[`${study1}_vs_${study2}`] = transformed;
                        if (this._isMounted) this.setState(s);
                    });

                }
            }
        }
    }

    render(){
        for (const study1 of this.props.studies1) {
            for (const study2 of this.props.studies2) {
                if (study1 !== study2 && meta[study1][study2]["joint"] > Math.max(this.props.pc1, this.props.pc2) && this.state[`${study1}_vs_${study2}`] === undefined) {
                    return null;
                }
            }
        }
        let data = [];
        const shapes = [];
        const annotations = [];
        const layout = {autosize: true, showlegend: false,
            yaxis: { range: [0, 1], showgrid: false, showline: false, showticklabels: false},
            xaxis: { showgrid: false, showline: false, showticklabels: false, zeroline: false},
            grid: {
                rows: this.props.studies2.length,
                columns: this.props.studies1.length,
                pattern: "independent",
                xgap: 0.1,
                ygap: 0.1 
            },
            shapes: shapes,
            dragmode: false,
            margin: {
                l: 185,
                r: 0,
                t: 175,
                b: 30
            },
            annotations: annotations
        };
        let count = 1;
        for (const study2 of this.props.studies2) {
            for (const study1 of this.props.studies1) {
                if (study1 !== study2 && meta[study1][study2]["joint"] > Math.max(this.props.pc1, this.props.pc2)) {
                    data = data.concat([study1, study2].map((study) =>
                        this.props.separateCaseControl ?
                            ["cases", "controls"].map((c) =>
                            ({
                                x: this.state[`${study1}_vs_${study2}`][study][c][0],
                                y: this.state[`${study1}_vs_${study2}`][study][c][1],
                                type: "scattergl",
                                mode: "markers",
                                text: `${formatStudyName(study)} (${c.slice(0, c.length-1)})`,
                                xaxis: `x${count === 1 ? '' : count}`,
                                yaxis: `y${count === 1 ? '' : count}`,
                                hovertemplate: `${formatStudyName(study)} (${c.slice(0, c.length-1)})<extra></extra>`,
                                marker: {color: study === study1 ?
                                    (c === "controls" ? "green" : "red") :
                                    (c === "controls" ? "blue" : "yellow"),
                                    size: this.props.markerSize,
                                    opacity: this.props.opacity
                                }
                            })
                            ) :
                            {
                                x: this.state[`${study1}_vs_${study2}`][study]["both"][0],
                                y: this.state[`${study1}_vs_${study2}`][study]["both"][1],
                                type: "scattergl",
                                mode: "markers",
                                text: `${formatStudyName(study)}`,
                                xaxis: `x${count === 1 ? '' : count}`,
                                yaxis: `y${count === 1 ? '' : count}`,
                                hovertemplate: `${formatStudyName(study)}<extra></extra>`,
                                marker: {color: study === study1 ? "green" : "blue",
                                    size: this.props.markerSize,
                                    opacity: this.props.opacity
                                }
                            }
                    ).flat());
                    const maximal = [this.state[`${study1}_vs_${study2}`][study1]["both"].flat(), this.state[`${study1}_vs_${study2}`][study2]["both"].flat()].flat().map(x => Math.abs(x)).reduce((x, y) => Math.max(x, y), 0);
                    layout[`xaxis${count === 1 ? '' : count}`] = { range: [-maximal, maximal], showticklabels: false};
                    layout[`yaxis${count === 1 ? '' : count}`] = { range: [-maximal, maximal], showticklabels: false};
                }
                count++;
            }
        }
        [this.props.studies2, 1].flat().forEach((e, i) => {
            shapes.push({
                x0: -0.30,
                y0: ((1 + 0.1/this.props.studies2.length)*i-0.05) / this.props.studies2.length,
                x1: 1 + 0.05 / this.props.studies1.length,
                y1: ((1 + 0.1/this.props.studies2.length)*i-0.05) / this.props.studies2.length,
                type: "line",
                xref: "paper",
                yref: "paper"
            });
        });
        [this.props.studies1, 1].flat().forEach((e, i) => {
            shapes.push({
                x0: ((1 + 0.1/this.props.studies1.length)*i-0.05) / this.props.studies1.length,
                y0: -0.05 / this.props.studies2.length,
                x1: ((1 + 0.1/this.props.studies1.length)*i-0.05) / this.props.studies1.length,
                y1: 1.30,
                type: "line",
                xref: "paper",
                yref: "paper"
            });
        });
        this.props.studies1.forEach((e, i) => {
            annotations.push({
                x: ((1 + 0.1/this.props.studies1.length)*(i+0.5) - 0.05) / this.props.studies1.length + 0.01,
                y: 1.05,
                text: formatStudyName(e),
                xref: "paper",
                yref: "paper",
                yanchor: "bottom",
                xanchor: "right",
                showarrow: false,
                textangle: -90
            });
        }); 
        this.props.studies2.forEach((e, i) => {
            annotations.push({
                x: -0.05,
                y: ((1 + 0.1/this.props.studies2.length)*(this.props.studies2.length-i-0.5)-0.05) / this.props.studies2.length,
                text: formatStudyName(e),
                xref: "paper",
                yref: "paper",
                yanchor: "middle",
                xanchor: "right",
                showarrow: false,
                textangle: 0
            });
        });   
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}} layout={layout} />);
    }
}

export default class PCADoubleMatrix extends Component{
    constructor(props){
        super(props);
        this.state = {
            pc1: 0,
            pc2: 1,
            studies1: [studies[0]],
            studies2: [studies[1]],
            separateCaseControl: false,
            pcaBase: "x-axis",
            markerSize: 5,
            opacity: 1
        };
        this.changePC1 = this.changePC1.bind(this);
        this.changePC2 = this.changePC2.bind(this);
        this.changeSeparateCaseControl = this.changeSeparateCaseControl.bind(this);
        this.changeStudies1 = this.changeStudies1.bind(this);
        this.changeStudies2 = this.changeStudies2.bind(this);
        this.changePCABase = this.changePCABase.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
        this.changeOpacity = this.changeOpacity.bind(this);
    }

    changeStudies1(new_studies1){
        this.setState({studies1: new_studies1});
    }

    changeStudies2(new_studies2){
        this.setState({studies2: new_studies2});
    }

    changePCABase(event){
        this.setState({pcaBase: event.target.value});
    }

    changePC1(event){
        this.setState({pc1: parseInt(event.target.value)});
    }
    
    changePC2(event){
        this.setState({pc2: parseInt(event.target.value)});
    }

    changeSeparateCaseControl(event){
        this.setState({separateCaseControl: event.target.checked});
    }

    changeMarkerSize(event){
        this.setState({markerSize: parseInt(event.target.value)});
    }

    changeOpacity(event){
        this.setState({opacity: parseFloat(event.target.value)});
    }
    
    render(){
        return (
            <div className='row'>
                <div className='col-9'>
                    <PCADoubleMatrixPlot pc1={this.state.pc1} pc2={this.state.pc2} pcaBase={this.state.pcaBase}
                    separateCaseControl={this.state.separateCaseControl} studies1={this.state.studies1} studies2={this.state.studies2}
                    key={JSON.stringify(this.state)} markerSize={this.state.markerSize} opacity={this.state.opacity}/>
                </div>
                <div className='col-3'>
                    <Selection studies1={this.state.studies1} studies2={this.state.studies2}
                    pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl}
                    pcaBase={this.state.pcaBase} markerSize={this.state.markerSize}
                    opacity={this.state.opacity}
                    changeStudies1={this.changeStudies1} changeStudies2={this.changeStudies2}
                    changePC1={this.changePC1} changePC2={this.changePC2}
                    changeSeparateCaseControl={this.changeSeparateCaseControl}
                    changePCABase={this.changePCABase} changeMarkerSize={this.changeMarkerSize}
                    changeOpacity={this.changeOpacity}
                    />
                </div>
            </div>
        )
    }
}