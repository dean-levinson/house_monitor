import React, { Component } from "react";
import computerImage from "./images/computer.png";

export default class Computer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            ip: props.ip,
            ttl: props.ttl
        };
    }

    render() {
        return (
            <div className="computer">
                <div className="innerBox">
                    <img src={computerImage}></img>
                    <h3>Host {this.state.ip}</h3>
                </div>
                <ul className="computer">
                    <li className="computer">
                        ip: {this.state.ip}
                    </li>
                    <li className="computer">
                        ttl: {this.state.ttl}
                    </li>
                </ul>
            </div> 
        )
    }
}
