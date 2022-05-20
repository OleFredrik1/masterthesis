import { Component } from "react";
import { Link } from "react-router-dom";
import routing from '../Routes';
import Nav from 'react-bootstrap/Nav';
import NavItem from 'react-bootstrap/NavItem';
import NavLink from "react-bootstrap/NavLink";

export default class Menu extends Component {
    render() {
        return (
            <div className="min-vh-100 col-2 d-flex gap-2 flex-column justify-content-center align-items-center">
                {routing.map((route) =>
                    <Link className="w-100" key={route.path} to={route.path}>
                        <button className="w-100 btn btn-primary ms-2">{route.description}</button>
                    </Link>
                )}
            </div>
        );
    }
}