import { Component } from "react";
import { RightMenuCheckbox, RightMenuContainer, RightMenuSelector, RightMenuNumberInput } from "./RightMenu";
import Plot from "react-plotly.js";
import { formatStudyName } from "../Datasets";
import { studies } from "../Datasets";
import meta from "../data/LogFoldChange/meta.json";
import _ from "underscore";


class Selection extends Component{
    render(){
        return (
            <RightMenuContainer> 
                <RightMenuSelector label="Dataset 1" value={this.props.study1} onChange={this.props.changeStudy1}
                    optionValues={studies} optionNames={studies.map(formatStudyName)}
                    optionDisabled={studies.map(s => s == this.props.study2 || meta[s].indexOf(this.props.study2) === -1)} />
                 <RightMenuSelector label="Dataset 2" value={this.props.study2} onChange={this.props.changeStudy2}
                    optionValues={studies} optionNames={studies.map(formatStudyName)}
                    optionDisabled={studies.map(s => s == this.props.study1 || meta[this.props.study1].indexOf(s) === -1)} />
                <RightMenuNumberInput label="Marker size" min="1" max="20" value={this.props.markerSize} 
                    onChange={this.props.changeMarkerSize} oneLine={true}/>
            </RightMenuContainer>
        );
    }
}

class LogFoldChangePlot extends Component{
    constructor(props){
        super(props);
        this.state = {height: window.innerHeight};
    }

    componentWillUnmount(){
        window.removeEventListener("resize", this.updateSize.bind(this));
    }

    updateSize(){
        this.setState({height: window.innerHeight});
    }

    componentDidMount(){
        window.addEventListener("resize", this.updateSize.bind(this));
        fetch(`/data/LogFoldChange/${this.props.study1}_vs_${this.props.study2}.json`).then(r => r.json()).then(data =>{
            this.setState({data: data});
        });
    }

    render(){
        if (this.state.data == undefined) return null;
        const maximal = Math.max(...[this.state.data[this.props.study1], this.state.data[this.props.study2]].flat().map(Math.abs));
        const linspace = [...Array(100)].map((_, i) => 2*i*maximal/100 - maximal);
        const data = [{
            x: this.state.data[this.props.study1],
            y: this.state.data[this.props.study2],
            type: 'scatter',
            mode: 'markers',
            marker: {size: this.props.markerSize},
            text: this.state.data["mirnas"],
            customdata: _.zip(this.state.data["p-values"][this.props.study1], this.state.data["p-values"][this.props.study2]).map(v => ({
                s1: v[0].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>',
                s2: v[1].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>'
            })),
            hovertemplate: "<b>%{text}</b><br>" +
                           `p-value ${formatStudyName(this.props.study1)}: %{customdata.s1}<br>` +
                           `p-value ${formatStudyName(this.props.study2)}: %{customdata.s2}<br>` +
                           "<extra></extra>"
        },{
            type: "scatter",
            x: linspace,
            y: linspace.map(x => x * this.state.data["slope"] + this.state.data["intercept"]),
            mode: "lines",
            hovertemplate: `Slope: ${this.state.data["slope"].toFixed(2)}<br>`
                + `Intercept: ${this.state.data["intercept"].toFixed(2)}<br>`
                + `Correlation: ${this.state.data["corr"].toFixed(2)}<br>`
                + `p-value: ${this.state.data["p-value"].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>'}`
                + `<extra></extra>`
        }];
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={{title: `Log-fold-change plot of ${formatStudyName(this.props.study1)} and ${formatStudyName(this.props.study2)}`, autosize: true, showlegend: false,
                    xaxis: {range: [-maximal, maximal], title: `Log-fold-change of ${formatStudyName(this.props.study1)}`}, yaxis: {range: [-maximal, maximal], title: `Log-fold-change of ${formatStudyName(this.props.study2)}`}
                }} />
        );
    }
}

export default class LogFoldChange extends Component{
    constructor(props){
        super(props);
        this.state = {
            study1: studies[0],
            study2: studies[1],
            markerSize: 5 
        };
        this.changeStudy1 = this.changeStudy1.bind(this);
        this.changeStudy2 = this.changeStudy2.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
    }

    changeStudy1(event){
        this.setState({study1: event.target.value});
    }

    changeStudy2(event){
        this.setState({study2: event.target.value});
    }

    changeMarkerSize(event){
        this.setState({markerSize: parseInt(event.target.value)});
    }

    render(){
        return (
            <div className='row'>
                <div className='col-9'>
                    <LogFoldChangePlot study1={this.state.study1} study2={this.state.study2} key={JSON.stringify(this.state)}
                        markerSize={this.state.markerSize}/>
                </div>
                <div className='col-3'>
                    <Selection study1={this.state.study1} study2={this.state.study2} changeStudy1={this.changeStudy1}
                        changeStudy2={this.changeStudy2} changeMarkerSize={this.changeMarkerSize} markerSize={this.state.markerSize}
                    />
                </div>
            </div>
        );
    }
}