import './App.css';
import { Route, Routes } from 'react-router-dom';
import routing from './Routes';
import Menu from './components/menu';
import 'bootstrap/dist/css/bootstrap.min.css';
import datasets from './Datasets';

function EmptyCell(){
  return <div className='col-1' />
}

function App() {
  return (
    <div className='container-fluid'>
    <div className='row'>
      <Menu />
      <div className='col-10'>
        <Routes>
          {routing.map((route) =>
            <Route key={route.path} path={route.path} element={<route.element />} />
          )}
        </Routes>
      </div>
    </div>
    </div>
  );
}

export default App;
