import { Component } from "react";
import { RightMenuContainer, RightMenuSelector} from "./RightMenu";
import {studies, formatStudyName} from '../Datasets';
import meta from '../data/PairwiseMachineLearning/meta';
import Plot from "react-plotly.js";
import mldata from '../data/PairwiseMachineLearning/data.json';

class Selection extends Component{
    render() {
        return (
             <RightMenuContainer>
                <RightMenuSelector label="Dataset 1" value={this.props.study1} onChange={this.props.changeStudy1}
                    optionValues={studies} optionNames={studies.map(formatStudyName)}
                    optionDisabled={studies.map(s => s == this.props.study2 || meta[s].indexOf(this.props.study2) === -1)} />
                 <RightMenuSelector label="Dataset 2" value={this.props.study2} onChange={this.props.changeStudy2}
                    optionValues={studies} optionNames={studies.map(formatStudyName)}
                    optionDisabled={studies.map(s => s == this.props.study1 || meta[this.props.study1].indexOf(s) === -1)} />
                 <RightMenuSelector label="ML algorithm" value={this.props.algorithm} onChange={this.props.changeAlgorithm}
                    optionValues={["logreg", "SVM", "random forest", "xgb"]}
                    optionNames={["Logistic Regression", "SVM", "Random Forest", "XGBoost"]} />
             </RightMenuContainer>
        );
    }
}

class PairwiseMachineLearningPlot extends Component{
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
        const d = mldata[`${this.props.study1}_vs_${this.props.study2}`][this.props.algorithm];
        const s1 = this.props.study1;
        const s2 = this.props.study2;
        const data = [{
            x: [`Train: ${formatStudyName(s1)}<br>Test: ${formatStudyName(s1)}`, `Train: ${formatStudyName(s2)}<br>Test: ${formatStudyName(s2)}`, `Train: ${formatStudyName(s1)}<br>Test: ${formatStudyName(s2)}`, `Train: ${formatStudyName(s2)}<br>Test: ${formatStudyName(s1)}`],
            y: [d[s1], d[s2], d[`${s1} to ${s2}`], d[`${s2} to ${s1}`]],
            type: "bar"
        }];
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={{title: `Pairwise machine learning of ${formatStudyName(this.props.study1)} and ${formatStudyName(this.props.study2)}`, autosize: true, showlegend: false,
                    yaxis: {range: [0, 1], title: "AUC"}
                }} />
        );
    }
}

export default class PairwiseMachineLearning extends Component{
    constructor(props){
        super(props);
        this.state = {
            study1: studies[0],
            study2: studies[1],
            algorithm: "logreg"
        };
        this.changeStudy1 = this.changeStudy1.bind(this);
        this.changeStudy2 = this.changeStudy2.bind(this);
        this.changeAlgorithm = this.changeAlgorithm.bind(this);
    }

    changeStudy1(event){
        this.setState({study1: event.target.value});
    }

    changeStudy2(event){
        this.setState({study2: event.target.value});
    }

    changeAlgorithm(event){
        this.setState({algorithm: event.target.value});
    }

    render(){
        return (
            <div className='row'>
                <div className='col-9'>
                    <PairwiseMachineLearningPlot study1={this.state.study1} study2={this.state.study2} key={JSON.stringify(this.state)} algorithm={this.state.algorithm}/>
                </div>
                <div className='col-3'>
                    <Selection study1={this.state.study1} study2={this.state.study2} changeStudy1={this.changeStudy1}
                        changeStudy2={this.changeStudy2} changeAlgorithm={this.changeAlgorithm} algorithm={this.state.algorithm}
                    />
                </div>
            </div>
        );
    }

}

