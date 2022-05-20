import { Component } from "react";
import { RightMenuContainer, RightMenuMultiselect, RightMenuSelector} from "./RightMenu";
import {studies, formatStudyName} from '../Datasets';
import mldata from '../data/PairwiseMachineLearning/data.json';
import Plot from "react-plotly.js";

const meta = mldata["meta"];

class Selection extends Component{
    render() {
        return (
             <RightMenuContainer>
                <RightMenuMultiselect label="Datasets x-axis" value={this.props.studies1} onChange={this.props.changeStudies1}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                 <RightMenuMultiselect label="Datasets y-axis" value={this.props.studies2} onChange={this.props.changeStudies2}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                 <RightMenuSelector label="ML algorithm" value={this.props.algorithm} onChange={this.props.changeAlgorithm}
                    optionValues={["logreg", "SVM", "random forest", "xgb"]}
                    optionNames={["Logistic Regression", "SVM", "Random Forest", "XGBoost"]} />
             </RightMenuContainer>
        );
    }
}

class PairwiseMachineLearningMatrixPlot extends Component{
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

    render(){
        const data = [];
        let c = 1; 
        for (const s2 of this.props.studies2){
            for (const s1 of this.props.studies1){
                if (meta[s1].indexOf(s2) !== -1){
                    const t = mldata[`${s1}_vs_${s2}`][this.props.algorithm];
                    const indices = [s1, s2, `${s1} to ${s2}`, `${s2} to ${s1}`]
                    const y = indices.map(s => t[s]);
                    data.push({
                        x: [0, 1, 2, 3],
                        y: y,
                        type: "bar",
                        marker: {
                            color: y.map(x => `rgb(${255*(1-x)}, ${255*x}, 0)`)
                        },
                        xaxis: `x${c === 1 ? '' : c}`,
                        yaxis: `y${c === 1 ? '' : c}`,
                        text: [`Train: ${formatStudyName(s1)}<br>Test: ${formatStudyName(s1)}`, `Train: ${formatStudyName(s2)}<br>Test: ${formatStudyName(s2)}`, `Train: ${formatStudyName(s1)}<br>Test: ${formatStudyName(s2)}`, `Train: ${formatStudyName(s2)}<br>Test: ${formatStudyName(s1)}`],
                        textposition: "none",
                        hovertemplate: `<b>%{y}</b><br>%{text}<extra></extra>`
                    });
                }
                c++;
            }
        }
        const shapes = [];
        console.log(data);
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
        const annotations = [];
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
        console.log(annotations);   
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
        for (let i=2; i<c; i++){
            layout[`yaxis${i}`] = {range: [0, 1], showgrid: false, showline: false, showticklabels: false};
            layout[`xaxis${i}`] = { showgrid: false, showline: false, showticklabels: false, zeroline: false};
        }
        console.log(layout);
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={layout} config={{scrollZoom: false, displayModeBar: false}}/>
        );
    }
}

export default class PairwiseMachineLearningMatrix extends Component{
    constructor(props){
        super(props);
        this.state = {
            studies1: [studies[0]],
            studies2: [studies[1]],
            algorithm: "logreg"
        };
        this.changeStudies1 = this.changeStudies1.bind(this);
        this.changeStudies2 = this.changeStudies2.bind(this);
        this.changeAlgorithm = this.changeAlgorithm.bind(this);
    }

    changeStudies1(new_studies1){
        this.setState({studies1: new_studies1});
    }

    changeStudies2(new_studies2){
        this.setState({studies2: new_studies2});
    }

    changeAlgorithm(event){
        this.setState({algorithm: event.target.value});
    }

    render(){
        return (
            <div className='row'>
                <div className='col-9'>
                    <PairwiseMachineLearningMatrixPlot studies1={this.state.studies1} studies2={this.state.studies2} key={JSON.stringify(this.state)} algorithm={this.state.algorithm}/>
                </div>
                <div className='col-3'>
                    <Selection studies1={this.state.studies1} studies2={this.state.studies2} changeStudies1={this.changeStudies1}
                        changeStudies2={this.changeStudies2} changeAlgorithm={this.changeAlgorithm} algorithm={this.state.algorithm}
                    />
                </div>
            </div>
        );
    }

}

