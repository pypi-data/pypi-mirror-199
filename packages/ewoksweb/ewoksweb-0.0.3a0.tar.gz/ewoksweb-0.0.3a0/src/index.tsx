import { StrictMode } from 'react';
import ReactDOM from 'react-dom';
import { HashRouter, Routes, Route } from 'react-router-dom';

import 'normalize.css';
import './styles/index.css';

import App from './App';
import EwoksUiInfo from './Components/Frontpage/EwoksUiInfo';
import ExecutionTable from './Components/Execution/ExecutionTable';

ReactDOM.render(
  <StrictMode>
    <HashRouter>
      <Routes>
        <Route path="/" element={<EwoksUiInfo />} />
        <Route path="/edit-workflows" element={<App />} />
        <Route path="/monitor-workflows" element={<ExecutionTable />} />
      </Routes>
    </HashRouter>
  </StrictMode>,
  document.querySelector('#root')
);
