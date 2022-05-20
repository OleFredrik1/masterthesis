import {Component} from 'react';
import {studies, formatStudyName} from '../Datasets';
//import PCA from 'pca-js';
import Plot from 'react-plotly.js';
//import * as d3 from 'd3';
import meta from '../data/Boxplot/meta.json';
import { RightMenuContainer, RightMenuDataList, RightMenuSelector } from './RightMenu';

class Selection extends Component {
    constructor(props){
        super(props);
        this.state = {mirnaOrder: "lexical"};
        this.changemirnaOrder = this.changemirnaOrder.bind(this);
    }

    changemirnaOrder(event){
        this.setState({mirnaOrder: event.target.value});
    }

    render() {
        const mirnas = {
            lexical: x => x.sort(),
            "p-value inc": x => x.sort((a, b) => meta["p-values"][a] - meta["p-values"][b]),
            "p-value dec": x => x.sort((a, b) => meta["p-values"][b] - meta["p-values"][a]),
        }[this.state.mirnaOrder](meta.mirnas.slice()); 
        return (
            <RightMenuContainer>
                <RightMenuSelector label="Dataset ordering" value={this.props.datasetOrder} onChange={this.props.changeDatasetOrder}
                    optionValues={["lexical", "p-value", "separation"]} optionNames={["Alphabetical", "p-value", "Separation"]} />
                <RightMenuSelector label="Selector ordering" value={this.state.mirnaOrder} onChange={this.changemirnaOrder}
                    optionValues={["lexical", "p-value inc", "p-value dec"]} optionNames={["Alphabetical", "p-value (increasing)", "p-value (decreasing)"]} />
                <RightMenuDataList label="miRNA-sequence" value={this.props.mirna} onChange={this.props.changeMiRNA}
                    optionValues={mirnas} optionNames={mirnas.map(x => `p-value: ${meta["p-values"][x].toExponential(2).replace(/e\+?/, ' x 10^')}`)}/>
            </RightMenuContainer>
        )
    }
}

class BoxplotPlot extends Component{
 
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
        if (meta.mirnas.indexOf(this.props.mirna) !== -1)
        fetch(`/data/Boxplot/${this.props.mirna}.json`).then(r => r.json()).then(data =>{
            this.setState({data: data});
        });
    }
    
    render(){
        if (this.state.data == undefined) return null;
        console.log(this.state.data["p-values"]);
        const xOrder = [... new Set(this.state.data["controls"]["studies"])].sort((x, y) => ({
            "lexical": x.localeCompare(y),
            "p-value": this.state.data["p-values"][x] - this.state.data["p-values"][y],
            "separation": this.state.data["separation"][x] - this.state.data["separation"][y]
        }[this.props.datasetOrder]));
        console.log(xOrder);
        const data = [{
            x: this.state.data["controls"]["studies"].map(formatStudyName),
            y: this.state.data["controls"]["values"],
            name: "Controls",
            type: "box",
            marker: {color: "green"},
            hoverinfo: "none"
        },{
            x: this.state.data["cases"]["studies"].map(formatStudyName),
            y: this.state.data["cases"]["values"],
            name: "Cases",
            type: "box",
            marker: {color: "red"},
            hoverinfo: "none"
        }];
        const maximal = Math.max(...[this.state.data["controls"]["values"], this.state.data["cases"]["values"]].flat().map(Math.abs));
        data.push({
            type: 'bar',
            x: xOrder.map(formatStudyName),
            y: xOrder.map(x => 0),
            opacity: 0,
            showlegend: false,
            meta: xOrder.map(study => ({sequences: meta[study].mirnas, cases: meta[study].cases, controls: meta[study].controls, pvalue: this.state.data["p-values"][study].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>'})),
            hovertemplate: "<b>%{x}</b><br><br>"
                         + "Number of MiRNA-sequences: %{meta.sequences}<br>"
                         + "Number of cases: %{meta.cases}<br>"
                         + "Number of controls: %{meta.controls}<br>"
                         + "p-value of t-test: %{meta.pvalue}<br>"
                         + "<extra></extra>",
            marker:{
                color: "#f0f0f0"
            }
        });
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={{title: `<b>Boxplot of ${this.props.mirna}</b><br>p-value of t-test (all datasets combined): ${meta["p-values"][this.props.mirna].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>'}`, autosize: true, yaxis: {title: "Expression", range: [-maximal, maximal]}, xaxis: {categoryarray: xOrder.map(formatStudyName), categoryorder:"array"},
                    boxmode: "group", hovermode: "x", xhovermode: "none"
                }} />);
    }
}

export default class Boxplot extends Component{
    constructor(props){
        super(props);
        this.state = {
            mirna: meta.mirnas[0],
            datasetOrder: "lexical"
        };
        this.changeMiRNA = this.changeMiRNA.bind(this);
        this.changeDatasetOrder = this.changeDatasetOrder.bind(this);
    }

    changeMiRNA(event){
        this.setState({mirna: event.target.value});
    }

    changeDatasetOrder(event){
        this.setState({datasetOrder: event.target.value});
    }
    
    render(){
        return (
            <div className='row'>
                <div className='col-9'>
                    <BoxplotPlot mirna={this.state.mirna} key={JSON.stringify(this.state)} datasetOrder={this.state.datasetOrder}/>
                </div>
                <div className='col-3'>
                    <Selection mirna={this.state.mirna} changeMiRNA={this.changeMiRNA} datasetOrder={this.state.datasetOrder}
                    changeDatasetOrder={this.changeDatasetOrder}
                    />
                </div>
            </div>
        )
    }
}