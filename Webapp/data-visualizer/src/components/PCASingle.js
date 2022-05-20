import react, {Component} from 'react';
import datasets, {studies, formatStudyName} from '../Datasets';
//import PCA from 'pca-js';
import Plot from 'react-plotly.js';
//import * as d3 from 'd3';
import meta from '../data/PCASingle/meta.json';
import {RightMenuContainer, RightMenuRow, RightMenuSelector, RightMenuCheckbox, RightMenuNumberInput} from './RightMenu';

class Selection extends Component {
    render() {
        return (
            <RightMenuContainer>
                <RightMenuSelector label="Dataset" value={this.props.study} onChange={this.props.changeStudy}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                <RightMenuSelector label="PC x-axis" value={this.props.pc1} onChange={this.props.changePC1}
                    optionValues={[...Array(meta.numberOfComponents[this.props.study])].map((_, i) => i)}
                    optionNames={[...Array(meta.numberOfComponents[this.props.study])].map((_, i) => i + 1)}
                    optionDisabled={[...Array(meta.numberOfComponents[this.props.study])].map((_, i) => this.props.pc2 == i)}
                    oneLine={true}
                    />
                <RightMenuSelector label="PC y-axis" value={this.props.pc2} onChange={this.props.changePC2}
                    optionValues={[...Array(meta.numberOfComponents[this.props.study])].map((_, i) => i)}
                    optionNames={[...Array(meta.numberOfComponents[this.props.study])].map((_, i) => i + 1)}
                    optionDisabled={[...Array(meta.numberOfComponents[this.props.study])].map((_, i) => this.props.pc1 == i)}
                    oneLine={true}
                    />
                <RightMenuNumberInput label="Marker size" min="1" max="20" value={this.props.markerSize} 
                    onChange={this.props.changeMarkerSize} oneLine={true}/>
                <RightMenuNumberInput label="Opacity" min="0" max="1" step="0.05" value={this.props.opacity} 
                    onChange={this.props.changeOpacity} oneLine={true}/> 
                <RightMenuCheckbox label="Separate case and controls" checked={this.props.separateCaseControl}
                    onChange={this.props.changeSeparateCaseControl} />
            </RightMenuContainer>
        )
    }
}

class PCASinglePlot extends Component{

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

    componentDidMount(){
        window.addEventListener("resize", this.updateSize.bind(this));
        fetch(`/data/PCASingle/${this.props.study}.json`).then(r => r.json()).then(data =>{
            this.setState({var_exp: [data["variance explained"][this.props.pc1], data["variance explained"][this.props.pc2]]});
            const transformed = [data[this.props.pc1.toString()], data[this.props.pc2.toString()]];
            if (this.props.separateCaseControl){
                const cancer_x = transformed[0].filter((_, ind) => data["cancer"][ind]);
                const cancer_y = transformed[1].filter((_, ind) => data["cancer"][ind]);
                const control_x = transformed[0].filter((_, ind) => !data["cancer"][ind]);
                const control_y = transformed[1].filter((_, ind) => !data["cancer"][ind]);
                this.setState({data: [cancer_x, cancer_y, control_x, control_y]});
                return;
            }
            this.setState({data: transformed});
        });    
    }

    componentWillUnmount(){
        window.removeEventListener("resize", this.updateSize.bind(this));
    }
    
    render(){
        if (this.state.data == undefined) return null;
        let data;
        if (this.props.separateCaseControl){
            const trace1 = {
                x: this.state.data[0],
                y: this.state.data[1],
                type: "scatter",
                mode: "markers",
                name: "Cases",
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            }
            const trace2 = {
                x: this.state.data[2],
                y: this.state.data[3],
                type: "scatter",
                mode: "markers",
                name: "Controls",
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            }
            data = [trace1, trace2];
        }
        else {
            data = [{
                x: this.state.data[0],
                y: this.state.data[1],
                type: 'scatter',
                mode: 'markers',
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            }];
        }
        const maximal = this.state.data.flat().map(x => Math.abs(x)).reduce((x, y) => Math.max(x, y), 0);
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={{title: `PCA plot of ${formatStudyName(this.props.study)}`, autosize: true, 
                    xaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc1 + 1} (Variance expl.: ${(100 * this.state.var_exp[0]).toFixed(1)}%)`}, yaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc2 + 1} (Variance expl.: ${(100 * this.state.var_exp[1]).toFixed(1)}%)`}
                }} />);
    }
}

export default class PCASingle extends Component{
    constructor(props){
        super(props);
        this.state = {
            pc1: 0,
            pc2: 1,
            study: studies[0],
            separateCaseControl: false,
            markerSize: 5,
            opacity: 1
        };
        this.changePC1 = this.changePC1.bind(this);
        this.changePC2 = this.changePC2.bind(this);
        this.changeSeparateCaseControl = this.changeSeparateCaseControl.bind(this);
        this.changeStudy = this.changeStudy.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
        this.changeOpacity = this.changeOpacity.bind(this);
    }

    changeStudy(event){
        this.setState(state => ({
            study: event.target.value,
            pc1: state.pc1 < meta.numberOfComponents[event.target.value] ? state.pc1 : (state.pc2 == 0 ? 1 : 0),
            pc2: state.pc2 < meta.numberOfComponents[event.target.value] ? state.pc2 : (state.pc1 == 1 ? 0 : 1)
        }));
    }

    changePC1(event){
        this.setState({pc1: parseInt(event.target.value)});
    }
    
    changePC2(event){
        this.setState({pc2: parseInt(event.target.value)});
    }

    changeSeparateCaseControl(event){
        console.log(event.target.checked);
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
                    <PCASinglePlot pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl} study={this.state.study}
                    key={JSON.stringify(this.state)} markerSize={this.state.markerSize} opacity={this.state.opacity}/>
                </div>
                <div className='col-3'>
                    <Selection study={this.state.study} pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl} markerSize={this.state.markerSize}
                    opacity={this.state.opacity} changeOpacity={this.changeOpacity}
                    changeStudy={this.changeStudy} changePC1={this.changePC1} changePC2={this.changePC2}
                    changeSeparateCaseControl={this.changeSeparateCaseControl} changeMarkerSize={this.changeMarkerSize}
                    />
                </div>
            </div>
        )
    }
}