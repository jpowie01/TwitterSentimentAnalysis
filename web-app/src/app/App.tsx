import * as React from 'react';
import logo from '../res/logo.svg';
import {SearchForm} from '../search/search-form';
import './App.css';

class App extends React.Component {
  public render() {
    return (
      <div className="App">
        <img src={logo} className="App-logo" alt="logo" />
        <SearchForm />
      </div>
    );
  }
}

export default App;
