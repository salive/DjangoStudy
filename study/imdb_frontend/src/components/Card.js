import { setShows } from "../App"


const Card = ({ id, title, year, rating, poster, description, is_series,
    setShows, shows, userShows, setUserShows }) => {
    const onClick = () => {
        console.log('Click')
    }
    const poster_url = 'http://localhost:8000' + poster

    const addUserShow = () => {
        const body = {
            'show_id': id
        }
        fetch('http://localhost:8000/api/show/' + id + '/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage['auth_token']
            },
            body: JSON.stringify(body)

        })
        setShows(shows)
        setUserShows([...userShows, id])
    }
    const deleteUserShow = () => {
        const body = {
            'show_id': id
        }
        /* fetch('http://localhost:8000/api/show/' + id + '/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage['auth_token']
            },
            body: JSON.stringify(body)

        }) */
        setShows(shows)
        setUserShows(userShows.filter(s => s !== id))
    }




    return (
        <div className="container">
            <div className="poster">
                <img src={poster_url} alt={title}></img>
                {localStorage['auth_token'] ?
                    <div className="actions">
                        <button className="info-btn">
                            Инфо
                        </button>
                        {userShows.includes(id) ?
                            <button className="delete-btn" onClick={deleteUserShow}>
                                Передумал смотреть
                            </button>
                            :
                            <button className="watch-btn" onClick={addUserShow}>
                                Посмотреть
                            </button>
                        }

                    </div>
                    :
                    <div className="actions">
                        <button className="info-btn">
                            Инфо
                        </button>
                    </div>}
            </div>


            <div className="info-box">
                <h3>{title}</h3>
                <h5><i>{is_series ? "Сериал" : "Фильм"}</i></h5>
                <h6><i>{year}</i></h6>
                <p> {description}
                </p>
            </div>




            <div className="rating">
                <h4>Рейтинг: {rating}</h4>
            </div>

            <div className="empty"></div>

        </div>
    )
}

export default Card
