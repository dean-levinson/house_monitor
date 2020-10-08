import React, { Component } from "react";
import Computers from "./Computers";

export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            computers: Computers
        };
    }

    render() {
        return (
            <div className="component-app">
                <Computers />
            </div>
        )
    }
}
