import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  componentDidCatch(error, errorInfo) {
    // Update state to indicate an error has occurred
    this.setState({ hasError: true });
    // You can also log the error to an error reporting service
    // console.error(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Render fallback UI
      return <h1>Something went wrong.</h1>;
    }
    // Render the child components
    return this.props.children;
  }
}

export default ErrorBoundary;
