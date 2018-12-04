import React, { Component } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";
import { logout } from "./util/api";

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
  componentDidCatch(error, info) {
    console.log(error);
    logout().then(this.setLoggedOut());
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
      var component = <Dashboard logout={this.setLoggedOut} is_admin={is_admin} />;
    } else {
      var component = <Login setLoggedIn={this.setLoggedIn} />;
    }
    return (
      <React.Fragment>
        {component}
        <ErrorDialog open={this.state.hasError} message={this.state.error.message} />
      </React.Fragment>
    );
  }
}

export default App;
