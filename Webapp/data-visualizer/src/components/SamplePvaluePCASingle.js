import react, {Component} from 'react';
import datasets, {studies, formatStudyName} from '../Datasets';
//import PCA from 'pca-js';
import Plot from 'react-plotly.js';
//import * as d3 from 'd3';
import meta from '../data/SamplePvaluePCA/Single/meta.json';
import {RightMenuContainer, RightMenuMultiselect, RightMenuSelector, RightMenuCheckbox, RightMenuNumberInput} from './RightMenu';

class Selection extends Component {
    render() {
        return (
            <RightMenuContainer>
                <RightMenuSelector label="Dataset for PCA" value={this.props.study} onChange={this.props.changeStudy}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} /> 
                <RightMenuMultiselect label="Datasets for loadings" value={this.props.loadings} onChange={this.props.changeLoadings}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                <RightMenuSelector label="ML algorithm" value={this.props.algorithm} onChange={this.props.changeAlgorithm}
                    optionValues={["logreg", "SVM", "random forest", "xgb"]}
                    optionNames={["Logistic Regression", "SVM", "Random Forest", "XGBoost"]} />
                <RightMenuSelector label="PC x-axis" value={this.props.pc1} onChange={this.props.changePC1}
                    optionValues={[...Array(10)].map((_, i) => i)}
                    optionNames={[...Array(10)].map((_, i) => i + 1)}
                    optionDisabled={[...Array(10)].map((_, i) => this.props.pc2 == i || i >= meta[this.props.study])}
                    oneLine={true}
                    />
                <RightMenuSelector label="PC y-axis" value={this.props.pc2} onChange={this.props.changePC2}
                    optionValues={[...Array(10)].map((_, i) => i)}
                    optionNames={[...Array(10)].map((_, i) => i + 1)}
                    optionDisabled={[...Array(10)].map((_, i) => this.props.pc1 == i || i >= meta[this.props.study])}
                    oneLine={true}
                    />
                <RightMenuNumberInput label="Scale loadings" min="1" max="20" step="0.25" value={this.props.loadingScale} 
                    onChange={this.props.changeLoadingScale} oneLine={true}/>
                <RightMenuNumberInput label="Marker size" min="1" max="20" value={this.props.markerSize} 
                    onChange={this.props.changeMarkerSize} oneLine={true}/> 
                <RightMenuNumberInput label="Opacity" min="0" max="1" step="0.05" value={this.props.opacity} 
                    onChange={this.props.changeOpacity} oneLine={true} /> 
                <RightMenuCheckbox label="Show samples" checked={this.props.showSamples}
                    onChange={this.props.changeShowSamples} />
                <RightMenuCheckbox label="Separate case and controls" checked={this.props.separateCaseControl}
                    onChange={this.props.changeSeparateCaseControl} />
            </RightMenuContainer>
        )
    }
}

class SamplePvaluePCASinglePlot extends Component{
   
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
        fetch(`/data/SamplePvaluePCA/Single/${this.props.study}_${this.props.algorithm}.json`).then(r => r.json()).then(data => {
            this.setState({data: data});
        });
    }

    componentWillUnmount(){
        window.removeEventListener("resize", this.updateSize.bind(this));
    }
    
    render(){
        const data = this.state.data;
        if (data == undefined) return null;
        const plot_data = this.props.showSamples ? (this.props.separateCaseControl ?
            [{
                x: data["data"][this.props.pc1.toString()]["controls"],
                y: data["data"][this.props.pc2.toString()]["controls"],
                type: "scatter",
                mode: "markers",
                name: `${formatStudyName(this.props.study)} controls`,
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            },{
                x: data["data"][this.props.pc1.toString()]["cases"],
                y: data["data"][this.props.pc2.toString()]["cases"],
                type: "scatter",
                mode: "markers",
                name: `${formatStudyName(this.props.study)} cases`,
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            }] : [{
                x: data["data"][this.props.pc1.toString()]["cases"].concat(
                    data["data"][this.props.pc1.toString()]["controls"]
                ),
                y: data["data"][this.props.pc2.toString()]["cases"].concat(
                    data["data"][this.props.pc2.toString()]["controls"]
                ),
                type: "scatter",
                mode: "markers",
                showlegend: false,
                name: `${formatStudyName(this.props.study)}`,
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            }]) : [];
        const loadings = data["studies"].filter((s, i) => this.props.loadings.indexOf(s) !== -1 && [data["loadings"][i][this.props.pc1], data["loadings"][i][this.props.pc2]].map(Math.abs).reduce((x, y) => x + y, 0) > 0.1);
        const shapes = loadings.map((s, i) => {
            i = data["studies"].indexOf(s);
            return ({
                x1: data["loadings"][i][this.props.pc1] * this.props.loadingScale,
                y1: data["loadings"][i][this.props.pc2] * this.props.loadingScale,
                x0: 0, y0: 0,
                type: "line",
                text: formatStudyName(s),
                hoverinfo: "text"
            })
        });
        const annotations = loadings.map((s, i) => {
            i = data["studies"].indexOf(s); return ({
                x: data["loadings"][i][this.props.pc1] * this.props.loadingScale,
                y: data["loadings"][i][this.props.pc2] * this.props.loadingScale,
                ax: 0, ay: 0,
                text: formatStudyName(s),
                xanchor: "center",
                yanchor: "bottom"
            });
        });
        const maximal = plot_data.map(x => [x.x, x.y]).flat(2).map(x => Math.abs(x)).reduce((x, y) => Math.max(x, y), 0);
        console.log(maximal);
        return (
            <Plot data={plot_data} style={{width: "100%", height: this.state.height - 1}}
                layout={{title: `PCA plot of p-values`, autosize: true, 
                    xaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc1 + 1} (Variance expl.: ${(100 * this.state.data["variance explained"][this.props.pc1]).toFixed(1)}%)`}, yaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc2 + 1} (Variance expl.: ${(100 * this.state.data["variance explained"][this.props.pc2]).toFixed(1)}%)`}, shapes: shapes, annotations: annotations}} />);
    }
}

export default class SamplePvaluePCASingle extends Component{
    constructor(props){
        super(props);
        this.state = {
            pc1: 0,
            pc2: 1,
            study: studies[0],
            separateCaseControl: false,
            markerSize: 5,
            algorithm: "logreg",
            loadings: [],
            loadingScale: 2,
            showSamples: true,
            opacity: 1
        };
        this.changePC1 = this.changePC1.bind(this);
        this.changePC2 = this.changePC2.bind(this);
        this.changeSeparateCaseControl = this.changeSeparateCaseControl.bind(this);
        this.changeStudy = this.changeStudy.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
        this.changeAlgorithm = this.changeAlgorithm.bind(this);
        this.changeLoadings = this.changeLoadings.bind(this);
        this.changeLoadingScale = this.changeLoadingScale.bind(this);
        this.changeShowSamples = this.changeShowSamples.bind(this);
        this.changeOpacity = this.changeOpacity.bind(this);
    }

    changeStudy(event){
        this.setState({study: event.target.value});
    }

    changeAlgorithm(event){
        this.setState({algorithm: event.target.value});
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
    
    changeLoadings(new_loadings){
        this.setState({loadings: new_loadings});
    }

    changeLoadingScale(event){
        this.setState({loadingScale: parseFloat(event.target.value)});
    }

    changeShowSamples(event){
        this.setState({showSamples: event.target.checked});
    }

    changeOpacity(event){
        this.setState({opacity: parseFloat(event.target.value)});
    }

    render(){
        console.log(this.state);
        return (
            <div className='row'>
                <div className='col-9'>
                    <SamplePvaluePCASinglePlot pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl} study={this.state.study}
                    key={JSON.stringify(this.state)} markerSize={this.state.markerSize} algorithm={this.state.algorithm}
                    loadings={this.state.loadings} loadingScale={this.state.loadingScale}
                    showSamples={this.state.showSamples} opacity={this.state.opacity}/>
                </div>
                <div className='col-3'>
                    <Selection study={this.state.study} pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl} markerSize={this.state.markerSize}
                    loadings={this.state.loadings} opacity={this.state.opacity}
                    changeStudy={this.changeStudy} changePC1={this.changePC1} changePC2={this.changePC2}
                    changeSeparateCaseControl={this.changeSeparateCaseControl} changeMarkerSize={this.changeMarkerSize}
                    algorithm={this.state.algorithm} changeAlgorithm={this.changeAlgorithm} changeLoadings={this.changeLoadings}
                    changeLoadingScale={this.changeLoadingScale} loadingScale={this.state.loadingScale}
                    showSamples={this.state.showSamples} changeShowSamples={this.changeShowSamples}
                    changeOpacity={this.changeOpacity}
                    />
                </div>
            </div>
        )
    }
}