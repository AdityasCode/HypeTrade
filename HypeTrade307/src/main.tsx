import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "./index.css"
import App from './App.tsx'
import { MyAppErrorBoundary } from 'src/components/MyAppErrorBoundary.tsx'

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <MyAppErrorBoundary>
            <App />
        </MyAppErrorBoundary>
    </StrictMode>,
)