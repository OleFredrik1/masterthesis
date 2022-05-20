import react, {Component, lazy} from 'react';
import {studies, formatStudyName} from '../Datasets';
//import PCA from 'pca-js';
import Plot from 'react-plotly.js';
//import * as d3 from 'd3';
import meta from '../data/PCADouble/meta.json';
import {RightMenuContainer, RightMenuCheckbox, RightMenuSelector, RightMenuNumberInput} from './RightMenu';

class Selection extends Component {
    render() {
        if (meta[this.props.study1][this.props.study2][this.props.pcaBase] == -1) return null;
        return (
            <RightMenuContainer>
                <RightMenuSelector label="Dataset 1" value={this.props.study1} onChange={this.props.changeStudy1}
                    optionValues={studies} optionNames={studies.map(formatStudyName)}
                    optionDisabled={studies.map(s => s == this.props.study2 || meta[s][this.props.study2]["joint"] == -1)} />
                 <RightMenuSelector label="Dataset 2" value={this.props.study2} onChange={this.props.changeStudy2}
                    optionValues={studies} optionNames={studies.map(formatStudyName)}
                    optionDisabled={studies.map(s => s == this.props.study1 || meta[this.props.study1][s]["joint"] == -1)} />
                 <RightMenuSelector label="PCA based on" value={this.props.pcaBase} onChange={this.props.changePCABase}
                    optionValues={[this.props.study1, this.props.study2, "joint"]}
                    optionNames={[formatStudyName(this.props.study1), formatStudyName(this.props.study2), "Both"]} />
                <RightMenuSelector label="PC x-axis" value={this.props.pc1} onChange={this.props.changePC1}
                    optionValues={[...Array(meta[this.props.study1][this.props.study2][this.props.pcaBase])].map((_, i) => i)}
                    optionNames={[...Array(meta[this.props.study1][this.props.study2][this.props.pcaBase])].map((_, i) => i + 1)}
                    optionDisabled={[...Array(meta[this.props.study1][this.props.study2][this.props.pcaBase])].map((_, i) => this.props.pc2 == i)}
                    oneLine={true}
                    />
                <RightMenuSelector label="PC y-axis" value={this.props.pc2} onChange={this.props.changePC2}
                    optionValues={[...Array(meta[this.props.study1][this.props.study2][this.props.pcaBase])].map((_, i) => i)}
                    optionNames={[...Array(meta[this.props.study1][this.props.study2][this.props.pcaBase])].map((_, i) => i + 1)}
                    optionDisabled={[...Array(meta[this.props.study1][this.props.study2][this.props.pcaBase])].map((_, i) => this.props.pc1 == i)}
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

class PCADoublePlot extends Component{

    constructor(props){
        super(props);
        this.state = {
            data: undefined,
            height: window.innerHeight
        };
    }

    updateSize(){
        this.setState({height: window.innerHeight});
    }

    componentWillUnmount(){
        window.removeEventListener("resize", this.updateSize.bind(this));
    }

    componentDidMount(){
        window.addEventListener("resize", this.updateSize.bind(this));
        fetch(`/data/PCADouble/${this.props.study1}_vs_${this.props.study2}.json`).then(r => r.json()).then(data =>{
            data = data[this.props.pcaBase];
            console.log(data);
            const transformed = {};
            [this.props.study1, this.props.study2].forEach(s => {
                transformed[s] = {};
                transformed[s]["both"] = [data[s][this.props.pc1], data[s][this.props.pc2]];
                transformed[s]["cases"] = [data[s][this.props.pc1].filter((_, ind) => data[s]["cancer"][ind]),
                    data[s][this.props.pc2].filter((_, ind) => data[s]["cancer"][ind])];
                transformed[s]["controls"] = [data[s][this.props.pc1].filter((_, ind) => !data[s]["cancer"][ind]),
                    data[s][this.props.pc2].filter((_, ind) => !data[s]["cancer"][ind])];
            }); 
            this.setState({
                data: transformed,
                var_exp: [data["variance explained"][this.props.pc1], data["variance explained"][this.props.pc2]]
            });
        });
    }
    
    render(){
        if (this.state.data == undefined) return null;
        console.log(this.state.data);
        const data = [this.props.study1, this.props.study2].map((study) => 
            this.props.separateCaseControl ?
            ["cases", "controls"].map((c) =>
                ({ 
                    x: this.state.data[study][c][0],
                    y: this.state.data[study][c][1],
                    type: "scatter",
                    mode: "markers",
                    name: `${formatStudyName(study)} ${c}`,
                    marker: {size: this.props.markerSize, opacity: this.props.opacity}
                })
            ) :
            {
                x: this.state.data[study]["both"][0],
                y: this.state.data[study]["both"][1],
                type: "scatter",
                mode: "markers",
                name: `${formatStudyName(study)}`,
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            }
        ).flat();  
        const maximal = [this.state.data[this.props.study1]["both"].flat(), this.state.data[this.props.study2]["both"].flat()].flat().map(x => Math.abs(x)).reduce((x, y) => Math.max(x, y), 0);
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={{
                    title: `PCA plot of ${formatStudyName(this.props.study1)} and ${formatStudyName(this.props.study2)}`,      autosize: true, xaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc1 + 1} (Variance expl.: ${(100 * this.state.var_exp[0]).toFixed(1)}%)`}, yaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc2 + 1} (Variance expl.: ${(100 * this.state.var_exp[1]).toFixed(1)}%)`}
                }} />);
    }
}

export default class PCADouble extends Component{
    constructor(props){
        super(props);
        this.state = {
            pc1: 0,
            pc2: 1,
            study1: studies[0],
            study2: studies[1],
            separateCaseControl: false,
            pcaBase: studies[0],
            markerSize: 5,
            opacity: 1
        };
        this.changePC1 = this.changePC1.bind(this);
        this.changePC2 = this.changePC2.bind(this);
        this.changeSeparateCaseControl = this.changeSeparateCaseControl.bind(this);
        this.changeStudy1 = this.changeStudy1.bind(this);
        this.changeStudy2 = this.changeStudy2.bind(this);
        this.changePCABase = this.changePCABase.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
        this.changeOpacity = this.changeOpacity.bind(this);
    }

    changeStudy1(event){
        this.setState(state => ({
            study1: event.target.value,
            pcaBase: [event.target.value, state.study2, "joint"].indexOf(state.pcaBase) !== -1 ? state.pcaBase : event.target.value
        }));
    }

    changeStudy2(event){
        this.setState(state => ({
            study2: event.target.value,
            pcaBase: [event.target.value, state.study1, "joint"].indexOf(state.pcaBase) !== -1 ? state.pcaBase : state.study1
        }));
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
        console.log(this.state);
        return (
            <div className='row'>
                <div className='col-9'>
                    <PCADoublePlot pc1={this.state.pc1} pc2={this.state.pc2} pcaBase={this.state.pcaBase}
                    separateCaseControl={this.state.separateCaseControl} study1={this.state.study1} study2={this.state.study2}
                    key={JSON.stringify(this.state)} markerSize={this.state.markerSize} opacity={this.state.opacity}/>
                </div>
                <div className='col-3'>
                    <Selection study1={this.state.study1} study2={this.state.study2} pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl} opacity={this.state.opacity}
                    pcaBase={this.state.pcaBase} markerSize={this.state.markerSize}
                    changeStudy1={this.changeStudy1} changeStudy2={this.changeStudy2}
                    changePC1={this.changePC1} changePC2={this.changePC2} changeOpacity={this.changeOpacity}
                    changeSeparateCaseControl={this.changeSeparateCaseControl}
                    changePCABase={this.changePCABase} changeMarkerSize={this.changeMarkerSize}
                    />
                </div>
            </div>
        )
    }
}