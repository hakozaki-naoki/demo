import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

// index.html の <div id="root"></div> を取得してアプリを描画します
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)