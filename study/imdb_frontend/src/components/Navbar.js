import React from 'react'

import { useState } from "react";
import { MdLogout, MdLogin } from 'react-icons/md'
import SearchIcon from '@material-ui/icons/Search';

const Navbar = ({ fetchShows, setShows, fetchUserShows }) => {
    const [keyword, setKeyword] = useState();
    const handleSearch = async e => {
        e.preventDefault();
        const body = {
            'keyword': keyword
        }
        const res = await fetch('http://localhost:8000/api/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',

            },
            body: JSON.stringify(body)


        })
        const jsonRes = await res.json()


        const data = jsonRes.map((show) => ({
            "id": show.filmId,
            "title": show.nameRu,
            "year": show.year,
            "description": show.description,
            "poster": show.posterUrl,
            "rating": show.rating,
            "is_series": show.type === 'FILM' ? false : true,
            "img_web": true,
        }))
        setShows(data)
        setKeyword('')
    }





    return (
        <nav className="mynavbar">

            {localStorage['auth_token'] ?
                <ul className="mynav">

                    <li>
                        <h3 className="nav-item" onClick={() => { fetchShows('http://localhost:8000/api/films') }}>Фильмы</h3>
                    </li>
                    <li>
                        <h3 className="nav-item" onClick={() => { fetchShows('http://localhost:8000/api/series') }}>Сериалы</h3>
                    </li>
                    <li>
                        <h3 className="nav-item" onClick={() => { fetchUserShows('http://localhost:8000/api/user/shows') }}>Хочу посмотреть</h3>
                    </li>
                    <li>
                        <h3 className="nav-item" href="#">Мои оценки</h3>
                    </li>

                    <li>
                        <SearchIcon style={{ color: "white" }} />
                        <form method="get" className="nav-item" onSubmit={handleSearch}>
                            <input type="text" className="search" name="search" value={keyword} placeholder='Поиск...' onChange={e => setKeyword(e.target.value)} />

                        </form>
                    </li>

                </ul>
                :
                <ul className="mynav">
                    <li>
                        <h3 className="nav-item" onClick={() => { fetchShows('http://localhost:8000/api/films') }}>Фильмы</h3>
                    </li>
                    <li>
                        <h3 className="nav-item" onClick={() => { fetchShows('http://localhost:8000/api/series') }}>Сериалы</h3>
                    </li>

                </ul>
            }



            <div className="nav-footer">


                {localStorage['auth_token'] ?
                    <div className="logout-container">
                        <a className="nav-item login" href="/logout"><MdLogout size={30} color={'white'} title={'Выйти'} /></a>

                    </div>
                    :
                    <div className="login-container">
                        <a className="nav-item login" href="/login">Войти </a>
                    </div>
                }
            </div>


        </nav>
    )
}

export default Navbar
