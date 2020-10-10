import React, { Component } from "react";
import Computer from "./Computer";
import socketIOClient from "socket.io-client";
const ENDPOINT = "http://localhost:3000";

export default class Computers extends Component {
    constructor(props) {
        super(props);
        this.state = {
            sockets: [],
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
        //this.getComputers();
        const socket = socketIOClient(ENDPOINT);
        let sockets = this.state.sockets.slice();
        sockets.push(socket);
        this.setState({sockets: sockets})

        socket.on("FromAPI", data => {
            this.setState({computers: data});
        });
        console.log("mount: ", this.state.sockets);
    }

    componentWillUnmount() {
        console.log("unmount: ", this.state.sockets);
        for (let index = 0; index < this.state.sockets.length; index++) {
            this.state.sockets[index].disconnect();
        }
        this.setState({sockets: []});
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
