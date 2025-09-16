import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './stylesheets/index.css'
import App from './App.jsx'
import * as serviceWorker from './serviceWorker'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

serviceWorker.unregister();

//"start": "HOST='127.0.0.1' PORT='5000' react-scripts start",