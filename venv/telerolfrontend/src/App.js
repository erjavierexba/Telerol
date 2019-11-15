import React from 'react';
import Login from './components/Login/Login';
import { Provider } from 'react-redux';
import './App.css';
import { createStore } from 'redux';
import {SendMSG} from './components/Reducers/SendMsg';

const store = createStore(SendMSG,window.STATE_FROM_SERVER);
function App() {
  return (
    <Provider store={store}>
        <Login/>
    </Provider>
    
  );
}

export default App;
