import React, { Component } from "react";
import { logout } from "./util/api";
import ErrorDialog from "./ErrorDialog";

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: { message: "" } };
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true, error: error };
    }

    componentDidCatch(error, info) {
        console.log(error);
        if (error.code === 401) {
            logout().then(json => { this.props.setLoggedOut() });
        }
    }

    render() {
        return (
            <React.Fragment>
                {this.props.children}
                <ErrorDialog open={this.state.hasError} message={this.state.error.message} />
            </React.Fragment>
        );
    }
}

export default ErrorBoundary;
