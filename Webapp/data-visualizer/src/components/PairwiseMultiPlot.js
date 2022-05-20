import { Component } from "react";
import { studies, formatStudyName } from "../Datasets";
import { RightMenuContainer, RightMenuSelector, RightMenuNumberInput, RightMenuCheckbox } from "./RightMenu";
import metaPCA from "../data/PCADouble/meta.json";
import metaLogFoldChange from "../data/LogFoldChange/meta.json";
import metaML from "../data/PairwiseMachineLearning/meta.json";
import mlData from "../data/PairwiseMachineLearning/data.json";
import Plot from "react-plotly.js";
import _ from "underscore";

class Selection extends Component{
    render(){
        return (
            <RightMenuContainer> 
                <RightMenuSelector label="Dataset 1" value={this.props.study1} onChange={this.props.changeStudy1}
                    optionValues={studies} optionNames={studies.map(formatStudyName)}
                    optionDisabled={studies.map(s => s === this.props.study2)}/>
                <RightMenuSelector label="Dataset 2" value={this.props.study2} onChange={this.props.changeStudy2}
                    optionValues={studies} optionNames={studies.map(formatStudyName)}
                    optionDisabled={studies.map(s => s === this.props.study1)} />
                <RightMenuSelector label="ML algorithm" value={this.props.algorithm} onChange={this.props.changeAlgorithm}
                    optionValues={["logreg", "SVM", "random forest", "xgb"]}
                    optionNames={["Logistic Regression", "SVM", "Random Forest", "XGBoost"]} />
                <RightMenuSelector label="PCA based on" value={this.props.pcaBase} onChange={this.props.changePCABase}
                    optionValues={[this.props.study1, this.props.study2, "joint"]}
                    optionNames={[formatStudyName(this.props.study1), formatStudyName(this.props.study2), "Both"]} />
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
        );
    }
}

class PairwiseMultiPlotPlot extends Component{
    constructor(props){
        super(props);
        this.state = {height: window.innerHeight};
        this._isMount = false;
    }
    
    updateSize(){
        this.setState({height: window.innerHeight});
    }

    componentWillUnmount(){
        this._isMount = false;
        window.removeEventListener("resize", this.updateSize.bind(this));
    }

    componentDidMount() {
        window.addEventListener("resize", this.updateSize.bind(this));
        this._isMount = true;
        if (metaPCA[this.props.study1][this.props.study2]["joint"] >= Math.max(this.props.pc1, this.props.pc2)) {
            fetch(`/data/PCADouble/${this.props.study1}_vs_${this.props.study2}.json`).then(r => r.json()).then(data => {
                console.log(data);
                if (this._isMount) {
                    data = data[this.props.pcaBase];
                    const transformed = {};
                    [this.props.study1, this.props.study2].forEach(s => {
                        transformed[s] = {};
                        transformed[s]["both"] = [data[s][this.props.pc1], data[s][this.props.pc2]];
                        transformed[s]["cases"] = [data[s][this.props.pc1].filter((_, ind) => data[s]["cancer"][ind]),
                        data[s][this.props.pc2].filter((_, ind) => data[s]["cancer"][ind])];
                        transformed[s]["controls"] = [data[s][this.props.pc1].filter((_, ind) => !data[s]["cancer"][ind]),
                        data[s][this.props.pc2].filter((_, ind) => !data[s]["cancer"][ind])];
                    });
                    this.setState({ pcaData: transformed, var_exp: [data["variance explained"][this.props.pc1], data["variance explained"][this.props.pc2]] });
                }
            });
        }
        if (metaLogFoldChange[this.props.study1].indexOf(this.props.study2) !== -1){
            fetch(`/data/LogFoldChange/${this.props.study1}_vs_${this.props.study2}.json`).then(r => r.json()).then(data => {
                if (this._isMount) this.setState({logFoldChangeData: data});
            });
        }
        if (metaML[this.props.study1].indexOf(this.props.study2) !== -1){
            fetch(`/data/PairwiseMachineLearning/${this.props.study1}_vs_${this.props.study2}.json`).then(r => r.json()).then(data => {
                if (this._isMount) this.setState({mlData: data});
            });
        }
    }

    render(){
        const layout = {
            autosize: true,
            showlegend: false,
            grid: {
                rows: 2,
                columns: 2,
                pattern: "independent",
                xgap: 20,
                ygap: 20
            },
            shapes: [{
                x0: 0.475,
                y0: 0,
                x1: 0.475,
                y1: 1,
                type: "line",
                xref: "paper",
                yref: "paper"
            },{
                x0: 0,
                y0: 0.475,
                x1: 1,
                y1: 0.475,
                type: "line",
                xref: "paper",
                yref: "paper"
            }],
            margin: {
                l: 50,
                r: 0,
                b: 130,
                t: 50
            }
        };
        let data = [];
        if (this.state.pcaData !== undefined) {
            data = data.concat([this.props.study1, this.props.study2].map((study) =>
                this.props.separateCaseControl ?
                    ["cases", "controls"].map((c) =>
                    ({
                        x: this.state.pcaData[study][c][0],
                        y: this.state.pcaData[study][c][1],
                        type: "scatter",
                        mode: "markers",
                        name: `${formatStudyName(study)} ${c}`,
                        marker: { size: this.props.markerSize, opacity: this.props.opacity },
                        xaxis: "x",
                        yaxis: "y",
                        hovertemplate: `${formatStudyName(study)} ${c.slice(0, c.length - 1)}<extra></extra>`
                    })
                    ) :
                    {
                        x: this.state.pcaData[study]["both"][0],
                        y: this.state.pcaData[study]["both"][1],
                        type: "scatter",
                        mode: "markers",
                        name: `${formatStudyName(study)}`,
                        marker: { size: this.props.markerSize, opacity: this.props.opacity },
                        xaxis: "x",
                        yaxis: "y",
                        hovertemplate: formatStudyName(study)
                    }
            ).flat());
            const maximal = [this.state.pcaData[this.props.study1]["both"].flat(), this.state.pcaData[this.props.study2]["both"].flat()].flat().map(x => Math.abs(x)).reduce((x, y) => Math.max(x, y), 0);
            layout["xaxis"] = {range: [-maximal, maximal], title: `PC ${this.props.pc1 + 1} (Variance expl.: ${(100 * this.state.var_exp[0]).toFixed(1)}%)`};
            layout["yaxis"] = {range: [-maximal, maximal], title: `PC ${this.props.pc2 + 1} (Variance expl.: ${(100 * this.state.var_exp[1]).toFixed(1)}%)`};
        }
        if (this.state.logFoldChangeData !== undefined) {
            const maximal = Math.max(...[this.state.logFoldChangeData[this.props.study1], this.state.logFoldChangeData[this.props.study2]].flat().map(Math.abs));
            const linspace = [...Array(100)].map((_, i) => 2 * i * maximal / 100 - maximal);
            data = data.concat([{
                x: this.state.logFoldChangeData[this.props.study1],
                y: this.state.logFoldChangeData[this.props.study2],
                type: 'scatter',
                mode: 'markers',
                marker: { size: this.props.markerSize },
                text: this.state.logFoldChangeData["mirnas"],
                customdata: _.zip(this.state.logFoldChangeData["p-values"][this.props.study1], this.state.logFoldChangeData["p-values"][this.props.study2]).map(v => ({
                    s1: v[0].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>',
                    s2: v[1].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>'
                })),
                hovertemplate: "<b>%{text}</b><br>" +
                    `p-value ${formatStudyName(this.props.study1)}: %{customdata.s1}<br>` +
                    `p-value ${formatStudyName(this.props.study2)}: %{customdata.s2}<br>` +
                    "<extra></extra>",
                xaxis: "x2",
                yaxis: "y2"
            }, {
                type: "scatter",
                x: linspace,
                y: linspace.map(x => x * this.state.logFoldChangeData["slope"] + this.state.logFoldChangeData["intercept"]),
                mode: "lines",
                hovertemplate: `Slope: ${this.state.logFoldChangeData["slope"].toFixed(2)}<br>`
                    + `Intercept: ${this.state.logFoldChangeData["intercept"].toFixed(2)}<br>`
                    + `Correlation: ${this.state.logFoldChangeData["corr"].toFixed(2)}<br>`
                    + `p-value: ${this.state.logFoldChangeData["p-value"].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>'}`
                    + `<extra></extra>`,
                xaxis: "x2",
                yaxis: "y2"
            }]);
            layout["xaxis2"] = {range: [-maximal, maximal], title: `Log-fold-change of ${formatStudyName(this.props.study1)}`};
            layout["yaxis2"] = {range: [-maximal, maximal], title: `Log-fold-change of ${formatStudyName(this.props.study2)}`};
        }
        if (metaML[this.props.study1].indexOf(this.props.study2) !== -1) {
            const d = mlData[`${this.props.study1}_vs_${this.props.study2}`][this.props.algorithm];
            const s1 = this.props.study1;
            const s2 = this.props.study2;
            data = data.concat([{
                x: [`Train: ${formatStudyName(s1)}<br>Test: ${formatStudyName(s1)}`, `Train: ${formatStudyName(s2)}<br>Test: ${formatStudyName(s2)}`, `Train: ${formatStudyName(s1)}<br>Test: ${formatStudyName(s2)}`, `Train: ${formatStudyName(s2)}<br>Test: ${formatStudyName(s1)}`],
                y: [d[s1], d[s2], d[`${s1} to ${s2}`], d[`${s2} to ${s1}`]],
                type: "bar",
                xaxis: "x3",
                yaxis: "y3",
                hovertemplate: `<b>%{y}</b><br>%{x}<extra></extra>`
            }]);
            layout["yaxis3"] = {range: [0, 1], title: `AUC`};
        }
        return (
            <Plot data={data} layout={layout} style={{width: "100%", height: this.state.height - 1}} 
                config={{displayModeBar: false}}>
            </Plot>
            );
    }
}

export default class PairwiseMultiPlot extends Component{
    constructor(props){
        super(props);
        this.state = {
            study1: studies[0],
            study2: studies[1],
            pc1: 0,
            pc2: 1,
            pcaBase: studies[0],
            separateCaseControl: false,
            markerSize: 5,
            algorithm: "logreg",
            opacity: 1
        };
        this.changePC1 = this.changePC1.bind(this);
        this.changePC2 = this.changePC2.bind(this);
        this.changeSeparateCaseControl = this.changeSeparateCaseControl.bind(this);
        this.changeStudy1 = this.changeStudy1.bind(this);
        this.changeStudy2 = this.changeStudy2.bind(this);
        this.changePCABase = this.changePCABase.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
        this.changeAlgorithm = this.changeAlgorithm.bind(this);
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

    changeAlgorithm(event){
        this.setState({algorithm: event.target.value});
    }

    changeOpacity(event){
        this.setState({opacity: parseFloat(event.target.value)});
    }

    render(){
        return ( 
            <div className='row'>
                <div className='col-9'>
                    <PairwiseMultiPlotPlot pc1={this.state.pc1} pc2={this.state.pc2} study1={this.state.study1}
                    study2={this.state.study2} separateCaseControl={this.state.separateCaseControl} pcaBase={this.state.pcaBase}
                    key={JSON.stringify(this.state)} markerSize={this.state.markerSize} algorithm={this.state.algorithm}
                    opacity={this.state.opacity}
                    />
                </div>
                <div className='col-3'>
                    <Selection study1={this.state.study1} study2={this.state.study2} pc1={this.state.pc1} pc2={this.state.pc2} 
                    separateCaseControl={this.state.separateCaseControl} markerSize={this.state.markerSize} loadings={this.state.loadings} loadingScale={this.state.loadingScale} pcaBase={this.state.pcaBase} opacity={this.state.opacity}
                    changeStudies={this.changeStudies} changePC1={this.changePC1} changePC2={this.changePC2}
                    changeSeparateCaseControl={this.changeSeparateCaseControl} changeMarkerSize={this.changeMarkerSize}
                    algorithm={this.state.algorithm} changeAlgorithm={this.changeAlgorithm} changeStudy1={this.changeStudy1} changeStudy2={this.changeStudy2} changePCABase={this.changePCABase} changeOpacity={this.changeOpacity}
                    />
                </div>
            </div>
        );
    }
}