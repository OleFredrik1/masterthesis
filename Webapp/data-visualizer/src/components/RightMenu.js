import { Component } from "react";
import _ from 'underscore';
//import ReactSelect from 'react-select';
//import makeAnimated from 'react-select/animated';
import {MultiSelect} from 'react-multi-select-component';

export class RightMenuMultiselect extends Component{
    render () {
        const id = _.uniqueId("multiselect-");
        const options = _.zip(this.props.optionValues, this.props.optionNames).map(v => ({value: v[0], label: v[1]}));
        const values = this.props.value.map(s => ({value: s, label: this.props.optionNames[this.props.optionValues.indexOf(s)]}));
        const onChange = ((x) => this.props.onChange(x.map(y => y.value)));
        return (
            <div className="mb-3">
                <label htmlFor={id} className="form-label">
                    {this.props.label}
                </label>
                <MultiSelect options={options} id={id} value={values} onChange={onChange} valueRenderer={() => "Select..."}/>
            </div>
        );
    }
}

export class RightMenuContainer extends Component {
    render() {
        return (
            <div className="min-vh-100 d-flex gap-2 flex-column justify-content-center align-items-center">
                <div className='right-menu'>
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export class RightMenuRow extends Component {
    render() {
        return (
            <div className={["mb-3"].concat(this.props.classNames || []).join(" ")}>
                {this.props.children}
            </div>
        );
    }
}

export class RightMenuSelector extends Component{
    render() {
        const disabled = this.props.optionDisabled || this.props.optionValues.map(_ => false);
        const id = _.uniqueId("selector-");
        return this.props.oneLine ?
            (<RightMenuRow classNames={["row"]}>
                <label htmlFor={id} className='col-form-label col-6'>
                    {this.props.label}:
                </label>
                <div className="col-6">
                    <select id={id} className="form-select" value={this.props.value} onChange={this.props.onChange}>
                        {_.zip(this.props.optionValues, this.props.optionNames, disabled).map(v =>
                            <option key={v[0]} value={v[0]} disabled={v[2]}>{v[1]}</option>
                        )}
                    </select></div>
            </RightMenuRow>) :
            (<RightMenuRow>
                <label htmlFor={id} className='form-label'>
                    {this.props.label}
                </label>
                <select id={id} className="form-select" value={this.props.value} onChange={this.props.onChange}>
                    {_.zip(this.props.optionValues, this.props.optionNames, disabled).map(v =>
                        <option key={v[0]} value={v[0]} disabled={v[2]}>{v[1]}</option>
                    )}
                </select>
            </RightMenuRow>);
    }
}

export class RightMenuCheckbox extends Component{
    render(){
        const id = _.uniqueId("checkbox-");
        return (
            <RightMenuRow>
                <div className="form-check">
                    <input className="form-check-input" type="checkbox" checked={this.props.checked}
                        onChange={this.props.onChange} id={id}/>
                    <label className="form-check-label" htmlFor={id}>
                        {this.props.label}
                    </label>
                </div>
            </RightMenuRow>
        );
    }
}

export class RightMenuNumberInput extends Component {
    render() {
        const id = _.uniqueId("number-input-");
        return this.props.oneLine ?
            (<RightMenuRow classNames={["row"]}>
                <label className="col-form-label col-6" htmlFor={id}>
                        {this.props.label}:
                    </label>
                <div className="col-6">
                    <input className="form-control" type="number" value={this.props.value} min={this.props.min || false}
                        max={this.props.max || false} onChange={this.props.onChange} id={id} step={this.props.step || 1} />
                </div>
            </RightMenuRow>) :
            (<RightMenuRow>
                <label className="form-label" htmlFor={id}>
                    {this.props.label}
                </label>
                <input className="form-control" type="number" value={this.props.value} min={this.props.min || false}
                    max={this.props.max || false} onChange={this.props.onChange} id={id} step={this.props.step || 1} />
            </RightMenuRow>);
    }
}

export class RightMenuDataList extends Component{
    render(){
        const id_input = _.uniqueId("data-list-input-");
        const id_list = _.uniqueId("data-list-list-");
        return (
            <RightMenuRow>
                <label htmlFor={id_input} className='form-label'>
                    {this.props.label}
                </label>
                <input className="form-control" id={id_input} list={id_list} value={this.props.value} onChange={this.props.onChange} />
                <datalist id={id_list}>
                    {_.zip(this.props.optionValues, this.props.optionNames).map(v =>
                        <option key={v[0]} value={v[0]}>{v[1]}</option>
                    )}
                </datalist>
            </RightMenuRow>
        )
    }
}