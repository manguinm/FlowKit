import React, { Component } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";
import { isLoggedIn, logout } from "./util/api";
import ErrorDialog from "./ErrorDialog";

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
    if (error.status_code === 401) {
      logout();
      this.setState({
        loggedIn: false,
        is_admin: false
      });
    }
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error: error };
  }
  logout = async () => {
    logout();
    this.setState({
      loggedIn: false,
      is_admin: false
    });
  }
  componentDidMount() {
    isLoggedIn().then(json => {
      this.setState({
        loggedIn: json.logged_in,
        is_admin: json.is_admin
      });
    });
  }
  render() {
    if (this.state.hasError) throw this.state.error;

    const { loggedIn, is_admin } = this.state;
    if (loggedIn) {
      var component = <Dashboard logout={this.logout} is_admin={is_admin} />;
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
