import React, { Component } from "react";
import ReactDOM from "react-dom";


class App extends Component {
    render() {
        return (
            <div className="component-app"> Hello World! </div>
        )
    }
}

ReactDOM.render(<App />, document.getElementById("root"))
