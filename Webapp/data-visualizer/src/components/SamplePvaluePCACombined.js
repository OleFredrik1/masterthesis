import react, {Component} from 'react';
import datasets, {studies, formatStudyName} from '../Datasets';
//import PCA from 'pca-js';
import Plot from 'react-plotly.js';
//import * as d3 from 'd3';
import pcadata from '../data/SamplePvaluePCA/Combined/data.json';
import {RightMenuContainer, RightMenuMultiselect, RightMenuSelector, RightMenuCheckbox, RightMenuNumberInput} from './RightMenu';

class Selection extends Component {
    render() {
        return (
            <RightMenuContainer>
                <RightMenuMultiselect label="Datasets for PCA" value={this.props.studies} onChange={this.props.changeStudies}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                <RightMenuMultiselect label="Datasets for loadings" value={this.props.loadings}
                    onChange={this.props.changeLoadings} optionValues={studies} optionNames={studies.map(formatStudyName)} />
                <RightMenuSelector label="ML algorithm" value={this.props.algorithm} onChange={this.props.changeAlgorithm}
                    optionValues={["logreg", "SVM", "random forest", "xgb"]}
                    optionNames={["Logistic Regression", "SVM", "Random Forest", "XGBoost"]} />
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
                <RightMenuNumberInput label="Scale loadings" min="1" max="20" step="0.25" value={this.props.loadingScale} 
                    onChange={this.props.changeLoadingScale} oneLine={true}/>
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

class SamplePvaluePCACombinedPlot extends Component{

    constructor(props){
        super(props);
        this.state = {height: window.innerHeight};
    }

    updateSize(){
        this.setState({height: window.innerHeight});
    }

    componentDidMount(){
        window.addEventListener("resize", this.updateSize.bind(this));
    }

    componentWillUnmount(){
        window.removeEventListener("resize", this.updateSize.bind(this));
    }

    render(){
        let data = this.props.studies.map(s => 
            this.props.separateCaseControl ?
            [{
                x: pcadata[this.props.algorithm]["data"][s][this.props.pc1.toString()]["controls"],
                y: pcadata[this.props.algorithm]["data"][s][this.props.pc2.toString()]["controls"],
                type: "scatter",
                mode: "markers",
                name: `${formatStudyName(s)} controls`,
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            },
            {
                x: pcadata[this.props.algorithm]["data"][s][this.props.pc1.toString()]["cases"],
                y: pcadata[this.props.algorithm]["data"][s][this.props.pc2.toString()]["cases"],
                type: "scatter",
                mode: "markers",
                name: `${formatStudyName(s)} cases`,
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            }] :
            [{
                x: pcadata[this.props.algorithm]["data"][s][this.props.pc1.toString()]["cases"].concat(
                    pcadata[this.props.algorithm]["data"][s][this.props.pc1.toString()]["controls"]
                ),
                y: pcadata[this.props.algorithm]["data"][s][this.props.pc2.toString()]["cases"].concat(
                    pcadata[this.props.algorithm]["data"][s][this.props.pc2.toString()]["controls"]
                ),
                type: "scatter",
                mode: "markers",
                showlegend: true,
                name: `${formatStudyName(s)}`,
                marker: {size: this.props.markerSize, opacity: this.props.opacity}
            }]).flat();
        const loadings = studies.filter((s, i) => this.props.loadings.indexOf(s) !== -1 && [pcadata[this.props.algorithm]["loadings"][i][this.props.pc1], pcadata[this.props.algorithm]["loadings"][i][this.props.pc2]].map(Math.abs).reduce((x, y) => x + y, 0) > 0.1);
        const shapes = loadings.map((s, i) => {
            i = studies.indexOf(s);
            return ({
                x1: pcadata[this.props.algorithm]["loadings"][i][this.props.pc1] * this.props.loadingScale,
                y1: pcadata[this.props.algorithm]["loadings"][i][this.props.pc2] * this.props.loadingScale,
                x0: 0, y0: 0,
                type: "line",
                text: formatStudyName(s),
                hoverinfo: "text"
            })
        });
        const annotations = loadings.map((s, i) => {
            i = studies.indexOf(s); return ({
                x: pcadata[this.props.algorithm]["loadings"][i][this.props.pc1] * this.props.loadingScale,
                y: pcadata[this.props.algorithm]["loadings"][i][this.props.pc2] * this.props.loadingScale,
                ax: 0, ay: 0,
                text: formatStudyName(s),
                xanchor: "center",
                yanchor: "bottom"
            });
        });
        const maximal = data.map(x => [x.x, x.y]).flat(2).map(x => Math.abs(x)).reduce((x, y) => Math.max(x, y), 0);
        console.log(maximal);
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={{title: `PCA plot of p-values`, autosize: true, 
                    xaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc1 + 1} (Variance expl.: ${(100 * pcadata[this.props.algorithm]["variance explained"][this.props.pc1]).toFixed(1)}%)`}, yaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc2 + 1} (Variance expl.: ${(100 * pcadata[this.props.algorithm]["variance explained"][this.props.pc2]).toFixed(1)}%)`},
                    shapes: shapes, annotations: annotations
                }} />);
    }
}

export default class SamplePvaluePCACombined extends Component{
    constructor(props){
        super(props);
        this.state = {
            pc1: 0,
            pc2: 1,
            studies: studies,
            separateCaseControl: false,
            markerSize: 5,
            algorithm: "logreg",
            loadings: [],
            loadingScale: 2,
            opacity: 1
        };
        this.changePC1 = this.changePC1.bind(this);
        this.changePC2 = this.changePC2.bind(this);
        this.changeSeparateCaseControl = this.changeSeparateCaseControl.bind(this);
        this.changeStudies = this.changeStudies.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
        this.changeAlgorithm = this.changeAlgorithm.bind(this);
        this.changeLoadings = this.changeLoadings.bind(this);
        this.changeLoadingScale = this.changeLoadingScale.bind(this);
        this.changeOpacity = this.changeOpacity.bind(this);
    }

    changeStudies(new_studies){
        this.setState({studies: new_studies});
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
        console.log(event.target.checked);
        this.setState({separateCaseControl: event.target.checked});
    }

    changeMarkerSize(event){
        this.setState({markerSize: parseInt(event.target.value)});
    }

    changeLoadings(new_loadings){
        this.setState({loadings: new_loadings});
    }

    changeLoadingScale(event){
        this.setState({loadingScale: parseFloat(event.target.value)})
    }

    changeOpacity(event){
        this.setState({opacity: parseFloat(event.target.value)});
    }
    
    render(){
        console.log(this.state);
        return (
            <div className='row'>
                <div className='col-9'>
                    <SamplePvaluePCACombinedPlot pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl} studies={this.state.studies}
                    key={JSON.stringify(this.state)} markerSize={this.state.markerSize} algorithm={this.state.algorithm}
                    loadings={this.state.loadings} loadingScale={this.state.loadingScale} opacity={this.state.opacity}
                    />
                </div>
                <div className='col-3'>
                    <Selection studies={this.state.studies} pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl} markerSize={this.state.markerSize} loadings={this.state.loadings} loadingScale={this.state.loadingScale} opacity={this.state.opacity}
                    changeStudies={this.changeStudies} changePC1={this.changePC1} changePC2={this.changePC2}
                    changeSeparateCaseControl={this.changeSeparateCaseControl} changeMarkerSize={this.changeMarkerSize}
                    algorithm={this.state.algorithm} changeAlgorithm={this.changeAlgorithm} changeLoadings={this.changeLoadings}
                    changeLoadingScale={this.changeLoadingScale} changeOpacity={this.changeOpacity}
                    />
                </div>
            </div>
        )
    }
}