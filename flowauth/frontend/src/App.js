import React, { Component } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";
import ErrorBoundary from "./ErrorBoundary";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loggedIn: false,
      is_admin: false,
      hasError: false,
      error: { message: "" }
    };
  }
  setLoggedIn = (is_admin) => {
    this.setState({
      loggedIn: true,
      is_admin: is_admin
    });
  }
  setLoggedOut = () => {
    this.setState({
      loggedIn: false,
      is_admin: false
    });
  }
  render() {
    if (this.state.hasError) throw this.state.error;

    const { loggedIn, is_admin } = this.state;
    if (loggedIn) {
      var component = <Dashboard setLoggedOut={this.setLoggedOut} is_admin={is_admin} />;
    } else {
      var component = <Login setLoggedIn={this.setLoggedIn} />;
    }
    return (
      <ErrorBoundary setLoggedOut={this.setLoggedOut} >
        {component}
      </ErrorBoundary>
    );
  }
}

export default App;
