

const Navbar = ({ fetchShows }) => {
    return (
        <nav className="mynavbar">
            <div className="nav-container">
                <a className="logo" href="/">Фильмотека &gt;</a>
                {localStorage['auth_token'] ?
                    <ul className="mynav">
                        <li>
                            <a className="mynavlink" href="/logout">Выйти</a>
                        </li>
                        <li>
                            <h6 className="mynavlink" onClick={() => { fetchShows('http://localhost:8000/api/films') }}>Фильмы</h6>
                        </li>
                        <li>
                            <h6 className="mynavlink" onClick={() => { fetchShows('http://localhost:8000/api/series') }}>Сериалы</h6>
                        </li>
                        <li>
                            <h6 className="mynavlink" onClick={() => { }}>Хочу посмотреть</h6>
                        </li>
                        <li>
                            <a className="mynavlink" href="#">Мои оценки</a>
                        </li>
                    </ul>
                    :
                    <ul className="mynav">
                        <li>
                            <a className="mynavlink" href="/login">Войти</a>
                        </li>
                        <li>
                            <h6 className="mynavlink" onClick={() => { fetchShows('http://localhost:8000/api/films') }}>Фильмы</h6>
                        </li>
                        <li>
                            <h6 className="mynavlink" onClick={() => { fetchShows('http://localhost:8000/api/series') }}>Сериалы</h6>
                        </li>

                    </ul>


                }

            </div>
        </nav>
    )
}

export default Navbar
