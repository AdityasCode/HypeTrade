//@ts-nocheck
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "./index.css"
import App from './App.tsx'

import { MyAppErrorBoundary } from './components/MyAppErrorBoundary';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <MyAppErrorBoundary>
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </MyAppErrorBoundary>
    </React.StrictMode>
);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
