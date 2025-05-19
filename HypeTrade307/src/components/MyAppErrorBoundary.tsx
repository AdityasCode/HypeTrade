import { Component, ReactNode } from 'react';

type ErrorBoundaryProps = { children: ReactNode };
type ErrorBoundaryState = { hasError: boolean };

export class MyAppErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
    constructor(props: ErrorBoundaryProps) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError() {
        return { hasError: true };          // switch to fallback UI
    }

    componentDidCatch(error: unknown, info: unknown) {
        console.error('Unhandled error:', error, info);  // log or send to Sentry
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: '2rem', textAlign: 'center' }}>
                    <h2>Something went wrong.</h2>
                    <p>Please refresh the page or try again.</p>
                </div>
            );
        }
        return this.props.children;
    }
}