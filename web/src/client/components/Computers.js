import React, { Component } from "react";
import Computer from "./Computer";

export default class Computers extends Component {
    constructor(props) {
        super(props);
        this.state = {
            computers: []
        };
    }

    getComputers() {
        fetch('/api/computers')
            .then(response => response.json())
            .then(payload => this.setState({computers: payload}))
            .catch(error => console.log("Error while fetching: ", error));
    }

    componentDidMount() {
        this.getComputers();
    }
//style={{"ListStyleType":"none"}}
    render() {
        return (
            <div className="app">
                <h1 className="head">house monitor dashboard</h1>
                <div className="computers">
                    <ul className="computers">  
                        { this.state.computers.map(computer => {
                            return (
                                <li key={computer.ip} className="computers"><Computer ip={computer.ip} ttl={computer.ttl} /> </li>
                            )
                        }) }
                    </ul>
                </div>
            </div>
        )
    }
}
