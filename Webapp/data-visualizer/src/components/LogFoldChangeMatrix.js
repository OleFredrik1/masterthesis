import { Component } from "react";
import { RightMenuCheckbox, RightMenuContainer, RightMenuSelector, RightMenuNumberInput, RightMenuMultiselect } from "./RightMenu";
import Plot from "react-plotly.js";
import { formatStudyName } from "../Datasets";
import { studies } from "../Datasets";
import meta from "../data/LogFoldChange/meta.json";
import _ from "underscore";


class Selection extends Component{
    render(){
        return (
            <RightMenuContainer> 
                <RightMenuMultiselect label="Datasets x-axis" value={this.props.studies1} onChange={this.props.changeStudies1}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                 <RightMenuMultiselect label="Datasets y-axis" value={this.props.studies2} onChange={this.props.changeStudies2}
                    optionValues={studies} optionNames={studies.map(formatStudyName)} />
                <RightMenuNumberInput label="Marker size" min="1" max="20" value={this.props.markerSize} 
                    onChange={this.props.changeMarkerSize} oneLine={true}/>
            </RightMenuContainer>
        );
    }
}

class LogFoldChangeMatrixPlot extends Component{
    constructor(props){
        super(props);
        this._isMounted = false;
        this.state = {height: window.innerHeight};
    }
    
    updateSize(){
        this.setState({height: window.innerHeight});
    }

    componentWillUnmount(){
        this._isMounted = false;
        window.removeEventListener("resize", this.updateSize.bind(this));
    }

    componentDidMount(){
        this._isMounted = true;
        for (const study1 of this.props.studies1){
            for (const study2 of this.props.studies2) {
                if (meta[study1].indexOf(study2) !== -1)
                fetch(`/data/LogFoldChange/${study1}_vs_${study2}.json`).then(r => r.json()).then(data => {
                    const s = {};
                    s[`${study1}_vs_${study2}`] = data;
                    if (this._isMounted) this.setState(s);
                });
            }
        }
        window.addEventListener("resize", this.updateSize.bind(this));
    }

    render(){
        for (const study1 of this.props.studies1){
            for (const study2 of this.props.studies2) {
                if (meta[study1].indexOf(study2) !== -1 && this.state[`${study1}_vs_${study2}`] == undefined) return null;
            }
        }
        let data = [];
        let c = 1;
        const layout = {
            autosize: true,
            showlegend: false,
            grid: {
                rows: this.props.studies2.length,
                columns: this.props.studies1.length,
                pattern: "independent",
                xgap: 0.1,
                ygap: 0.1 
            },
            margin: {
                l: 185,
                r: 0,
                b: 30,
                t: 175
            }
        };
        for (const study2 of this.props.studies2) {
            for (const study1 of this.props.studies1) {
                if (meta[study1].indexOf(study2) !== -1) {
                    const d = this.state[`${study1}_vs_${study2}`];
                    const maximal = Math.max(...[d[study1], d[study2]].flat().map(Math.abs));
                    const linspace = [...Array(100)].map((_, i) => 2 * i * maximal / 100 - maximal);
                    data = data.concat([{
                        x: d[study1],
                        y: d[study2],
                        type: 'scatter',
                        mode: 'markers',
                        marker: { size: this.props.markerSize },
                        text: d["mirnas"],
                        customdata: _.zip(d["p-values"][study1], d["p-values"][study2]).map(v => ({
                            s1: v[0].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>',
                            s2: v[1].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>'
                        })),
                        hovertemplate: "<b>%{text}</b><br>" +
                           `p-value ${formatStudyName(study1)}: %{customdata.s1}<br>` +
                           `p-value ${formatStudyName(study2)}: %{customdata.s2}<br>` +
                           "<extra></extra>",
                        xaxis: `x${c === 1 ? '' : c}`,
                        yaxis: `y${c === 1 ? '' : c}`
                    }, {
                        type: "scatter",
                        x: linspace,
                        y: linspace.map(x => x * d["slope"] + d["intercept"]),
                        mode: "lines",
                        hovertemplate: `<b>${formatStudyName(study1)} vs ${formatStudyName(study2)}</b><br>`
                            + `Slope: ${d["slope"].toFixed(2)}<br>`
                            + `Intercept: ${d["intercept"].toFixed(2)}<br>`
                            + `Correlation: ${d["corr"].toFixed(2)}<br>`
                            + `p-value: ${d["p-value"].toExponential(2).replace(/e\+?/, ' x 10<sup>') + '</sup>'}`
                            + `<extra></extra>`,
                        xaxis: `x${c === 1 ? '' : c}`,
                        yaxis: `y${c === 1 ? '' : c}`                       
                    }]);
                    layout[`xaxis${c === 1 ? '' : c}`] = {range: [-maximal, maximal], showticklabels: false};
                    layout[`yaxis${c === 1 ? '' : c}`] = {range: [-maximal, maximal], showticklabels: false};
                }
                c++;
            }
        }
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
        layout["annotations"] = annotations;
        const shapes = [];
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
        layout["shapes"] = shapes;
        return (
            <Plot data={data} style={{width: "100%", height: this.state.height - 1}}
                layout={layout} config={{scrollZoom: false, displayModeBar: false}}/>
        );
    }
}

export default class LogFoldChangeMatrix extends Component{
    constructor(props){
        super(props);
        this.state = {
            studies1: [studies[0]],
            studies2: [studies[1]],
            markerSize: 5 
        };
        this.changeStudies1 = this.changeStudies1.bind(this);
        this.changeStudies2 = this.changeStudies2.bind(this);
        this.changeMarkerSize = this.changeMarkerSize.bind(this);
    }

    changeStudies1(new_studies1){
        this.setState({studies1: new_studies1});
    }

    changeStudies2(new_studies2){
        this.setState({studies2: new_studies2});
    }

    changeMarkerSize(event){
        this.setState({markerSize: parseInt(event.target.value)});
    }

    render(){
        return (
            <div className='row'>
                <div className='col-9'>
                    <LogFoldChangeMatrixPlot studies1={this.state.studies1} studies2={this.state.studies2} 
                        key={JSON.stringify(this.state)} markerSize={this.state.markerSize}/>
                </div>
                <div className='col-3'>
                    <Selection studies1={this.state.studies1} studies2={this.state.studies2} changeStudies1={this.changeStudies1}
                        changeStudies2={this.changeStudies2} changeMarkerSize={this.changeMarkerSize} markerSize={this.state.markerSize}
                    />
                </div>
            </div>
        );
    }
}