import Navbar from './components/Navbar';
import './App.css';
import Cards from './components/Cards';
import { useState, useEffect } from 'react'

function App() {
  const [shows, setShows] = useState([])
  const [userShows, setUserShows] = useState([])

  // Получаем данные от бэкенда на этапе загрузки страницы
  useEffect(() => {
    const getShows = async () => {
      const shows = await fetchShows('http://localhost:8000/api')
    }
    const getUserShows = async () => {
      const userShows = localStorage['auth_token'] ? await fetchUserShows('http://localhost:8000/api/user/shows') : []
    }
    getShows()
    getUserShows()
  }, [])

  // Функция обращается к API бэкенда и получает данные из таблицы заказов
  const fetchShows = async (api_endpoint) => {
    const res = await fetch(api_endpoint)
    const data = await res.json()
    setShows(data)

  }
  const fetchUserShows = async (api_endpoint) => {
    const res = await fetch(api_endpoint, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + localStorage['auth_token']
      }


    })
    const data = await res.json()
    const userShowsArr = data.map((data) => data.show_id)
    setUserShows(userShowsArr)

  }
  return (
    <div className="App">
      <Navbar fetchShows={fetchShows} />
      <Cards userShows={userShows} setUserShows={setUserShows} setShows={setShows} shows={shows} fetchShows={fetchShows} />
    </div>
  );
}

export default App;
