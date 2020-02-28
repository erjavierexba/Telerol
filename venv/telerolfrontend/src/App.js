import React from 'react';
import {BrowserRouter as Router} from 'react-router-dom';
import {Login} from './components/Login/Login';
import { Provider } from 'react-redux';
import './App.css';
import { createStore } from 'redux';
import {send} from './components/Reducers/SendMsg';

export const store = createStore(send);
function App() {
  return (
    <div style={{background:'#e6e6e6',height:'inherit'}}>
      <Provider store={store}>
          <Router>
            <Login/>
          </Router>
      </Provider>
    </div>
  );
}

export default App;
