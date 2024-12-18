import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Main from './pages/main/main';
import Authorization from './pages/authorization/auth';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path={"/"} Component={Main}/>
        <Route path={"/auth"} Component={Authorization}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
