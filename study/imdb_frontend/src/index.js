import React from 'react';
import App from './App';
import Login from './components/Login';
import Logout from './components/Logout';
import {
  BrowserRouter,
  Routes,
  Route,
  Switch
} from "react-router-dom";
import { createRoot } from 'react-dom/client';
import NotFound from './components/NotFound';


const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="*" element={<NotFound />} />
      <Route path="/" element={<App />} />
      <Route path="/login" element={<Login />} />
      <Route path="/logout" element={<Logout />} />
    </Routes>
  </BrowserRouter>,

);



