import React, { Component } from 'react';
import './App.css';
import Person from './Person/Person';

class App extends Component {
  state = {
    persons: [
      {name: 'Rudi', age: 22},
      {name: 'Balls', age: 420}
    ]
  };

  switchNameHandler = () => {
    this.setState({
      persons: [
        {name: newName, age: 22},
        {name: 'Balls', age: 420}
      ]
    })
  }

  nameChangedHandler = (event) => {

  }

  render() {
    return (
      <div className="App">
        <h1>Ballsack</h1>
        <p>This is really working</p>
        <button onClick={this.switchNameHandler}>Switch Name</button>
        <Person
          name={this.state.persons[0].name}
          age={this.state.persons[0].age}/>
        <Person
          name={this.state.persons[1].name}
          age={this.state.persons[1].age}
          click={this.switchNameHandler}>Hobbies: Racing</Person>
      </div>
    );
  }
}

export default App;
