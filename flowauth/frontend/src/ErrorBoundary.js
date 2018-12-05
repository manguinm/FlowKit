import React, { Component } from "react";
import ErrorDialog from "./ErrorDialog";

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: { message: "" } };
    }

    clearError = () => {
        this.setState({ hasError: false, error: { message: "" } });
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true, error: error };
    }

    componentDidCatch(error, info) {
        console.log(error);
        if (error.code === 401) {
            this.props.setLoggedOut();
        }
    }

    render() {
        return (
            <React.Fragment>
                {this.props.children}
                <ErrorDialog
                    open={this.state.hasError}
                    onClose={this.clearError}
                    message={this.state.error.message}
                />
            </React.Fragment>
        );
    }
}

export default ErrorBoundary;
