// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;


import React from 'react';
import RegistrationForm from './components/Register';
import ProduceSubmissionForm from './components/ProduceSubmissionForm';

function App() {
  return (
    <div>
      <h1>Farm Produce App</h1>
      <RegistrationForm />
      <ProduceSubmissionForm />
    </div>
  );
}

export default App;
