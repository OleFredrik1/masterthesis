import {Component} from 'react';
import {studies, formatStudyName} from '../Datasets';
//import PCA from 'pca-js';
import Plot from 'react-plotly.js';
//import * as d3 from 'd3';
import pcadata from '../data/AUC_PCA/data.json';
import {RightMenuContainer, RightMenuMultiselect, RightMenuSelector, RightMenuCheckbox, RightMenuNumberInput} from './RightMenu';
import datasetMetadata from '../data/dataset_metadata.json';

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
                <RightMenuSelector label="Color coding" value={this.props.colorCoding} onChange={this.props.changeColorCoding}
                    optionNames={["None", "Technology", "Body fluid"]}
                    optionValues={["None", "Technology", "Body fluid"]} />
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
                    onChange={this.props.changeLoadingScale}  oneLine={true}/>
                <RightMenuNumberInput label="Marker size" min="1" max="20" value={this.props.markerSize} 
                    onChange={this.props.changeMarkerSize}  oneLine={true}/>
                <RightMenuNumberInput label="Opacity" min="0" max="1" step="0.05" value={this.props.opacity} 
                    onChange={this.props.changeOpacity} oneLine={true}/> 
                <RightMenuCheckbox label="Show dataset name" checked={this.props.showDatasetName}
                    onChange={this.props.changeShowDatasetName} />
            </RightMenuContainer>
        )
    }
}

class AUC_PCA_Plot extends Component {

    constructor(props){
        super(props);
        this.state = {height: window.innerHeight};
    }

    componentDidMount(){
        window.addEventListener("resize", this.updateSize.bind(this));
    }

    componentWillUnmount(){
        window.removeEventListener("resize", this.updateSize.bind(this));
    }

    updateSize(){
        this.setState({height: window.innerHeight});
    }

    render() {
        if (this.props.colorCoding === "None") {
            var data = [{
                x: this.props.studies.map(s => pcadata[this.props.algorithm]["data"][studies.indexOf(s)][this.props.pc1]),
                y: this.props.studies.map(s => pcadata[this.props.algorithm]["data"][studies.indexOf(s)][this.props.pc2]),
                type: "scatter",
                mode: this.props.showDatasetName ? "markers+text" : "markers",
                textposition: "bottom",
                text: this.props.studies.map(formatStudyName),
                marker: { size: this.props.markerSize, opacity: this.props.opacity }
            }];
        }
        else {
            const uniques = [...new Set(this.props.studies.map(s => datasetMetadata[s][this.props.colorCoding]))];
            var data = uniques.map(t => {
                const cur_studies = this.props.studies.filter(s => datasetMetadata[s][this.props.colorCoding] === t);
                return {
                    x: cur_studies.map(s => pcadata[this.props.algorithm]["data"][studies.indexOf(s)][this.props.pc1]),
                    y: cur_studies.map(s => pcadata[this.props.algorithm]["data"][studies.indexOf(s)][this.props.pc2]),
                    type: "scatter",
                    name: t,
                    mode: this.props.showDatasetName ? "markers+text" : "markers",
                    textposition: "bottom",
                    text: cur_studies.map(formatStudyName),
                    marker: { size: this.props.markerSize, opacity: this.props.opacity }
                };
            });
        }
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
        
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={{title: `PCA plot of AUC`, autosize: true, 
                    xaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc1 + 1} (Variance expl.: ${(100 * pcadata[this.props.algorithm]["variance explained"][this.props.pc1]).toFixed(1)}%)`}, yaxis: {range: [-maximal, maximal], title: `PC ${this.props.pc2 + 1} (Variance expl.: ${(100 * pcadata[this.props.algorithm]["variance explained"][this.props.pc2]).toFixed(1)}%)`},
                    shapes: shapes, annotations: annotations
                }} />);
    }
}

export default class AUC_PCA extends Component{
    constructor(props){
        super(props);
        this.state = {
            pc1: 0,
            pc2: 1,
            studies: studies,
            markerSize: 10,
            algorithm: "logreg",
            loadings: [],
            loadingScale: 2,
            showDatasetName: true,
            opacity: 1,
            colorCoding: "None"
        };
        this.changePC1 = this.changePC1.bind(this);
        this.changePC2 = this.changePC2.bind(this);
        this.changeStudies = this.changeStudies.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
        this.changeAlgorithm = this.changeAlgorithm.bind(this);
        this.changeLoadings = this.changeLoadings.bind(this);
        this.changeLoadingScale = this.changeLoadingScale.bind(this);
        this.changeShowDatasetName = this.changeShowDatasetName.bind(this);
        this.changeOpacity = this.changeOpacity.bind(this);
        this.changeColorCoding = this.changeColorCoding.bind(this);
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

    changeMarkerSize(event){
        this.setState({markerSize: parseInt(event.target.value)});
    }

    changeLoadings(new_loadings){
        this.setState({loadings: new_loadings});
    }

    changeLoadingScale(event){
        this.setState({loadingScale: parseFloat(event.target.value)})
    }

    changeShowDatasetName(event){
        this.setState({showDatasetName: event.target.checked});
    }

    changeOpacity(event){
        this.setState({opacity: parseFloat(event.target.value)});
    }

    changeColorCoding(event){
        this.setState({colorCoding: event.target.value});
    }
    
    render(){
        return (
            <div className='row'>
                <div className='col-9'>
                    <AUC_PCA_Plot pc1={this.state.pc1} pc2={this.state.pc2} studies={this.state.studies}
                    key={JSON.stringify(this.state)} markerSize={this.state.markerSize} algorithm={this.state.algorithm}
                    loadings={this.state.loadings} loadingScale={this.state.loadingScale} showDatasetName={this.state.showDatasetName} opacity={this.state.opacity} colorCoding={this.state.colorCoding}
                    />
                </div>
                <div className='col-3'>
                    <Selection studies={this.state.studies} pc1={this.state.pc1} pc2={this.state.pc2}
                    markerSize={this.state.markerSize} loadings={this.state.loadings} loadingScale={this.state.loadingScale}
                    showDatasetName={this.state.showDatasetName} opacity={this.state.opacity} colorCoding={this.state.colorCoding}
                    changeStudies={this.changeStudies} changePC1={this.changePC1} changePC2={this.changePC2}
                    changeMarkerSize={this.changeMarkerSize} changeOpacity={this.changeOpacity}
                    algorithm={this.state.algorithm} changeAlgorithm={this.changeAlgorithm} changeLoadings={this.changeLoadings}
                    changeLoadingScale={this.changeLoadingScale} changeShowDatasetName={this.changeShowDatasetName}
                    changeColorCoding={this.changeColorCoding}
                    />
                </div>
            </div>
        )
    }
}