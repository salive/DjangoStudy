import { setShows } from "../App"
import React from 'react'
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import DeleteIcon from '@material-ui/icons/Delete';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import KeyboardVoiceIcon from '@material-ui/icons/KeyboardVoice';
import Icon from '@material-ui/core/Icon';
import SaveIcon from '@material-ui/icons/Save';
import InfoIcon from '@material-ui/icons/Info';
import VisibilityIcon from '@material-ui/icons/Visibility';


const Card = ({ id, title, year, rating, poster, description, is_series,
    setShows, shows, userShows, setUserShows }) => {
    const onClick = () => {
        console.log('Click')
    }

    const countRatingBoxColor = (() => {
        if (rating >= 7) {
            return 'green'
        }
        else if (rating < 5) {
            return 'red'
        }
        else if (5 < rating < 7) {
            return 'orange'
        }


    })


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
        fetch('http://localhost:8000/api/show/' + id + '/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage['auth_token']
            },
            body: JSON.stringify(body)

        })
        setUserShows(userShows.filter(s => s !== id))
        setShows(shows.filter(s => userShows.includes(id)))

    }




    return (
        <div className="container">


            <h3 style={{ "max-width": "fit-content" }}>{title}</h3>
            <div className="header-info">
                <h5><i>{is_series ? "Сериал" : "Фильм"}, {year} </i></h5>
            </div>

            <div className="img-container">
                <img src={poster} alt={title}></img>
                <h2 className="rating-box" style={{ color: "white", "justify-content": "center", background: countRatingBoxColor() }}>{rating}</h2>
            </div>
            <p style={{ "max-width": "fit-content", "max-height": "100px", "overflow": "hidden", "text-overflow": "ellipsis", "margin-top": "10px" }}>{description}</p>
            {localStorage['auth_token'] ?
                <div className="actions">
                    {userShows.includes(id) ?
                        <div className="btn-box">
                            <Button
                                style={{ marginRight: "10px", background: '#0079ca' }}
                                variant="contained"
                                color="primary"
                                className='mu-button'
                                startIcon={<InfoIcon />}
                            >
                                Инфо
                            </Button>
                            <Button
                                onClick={deleteUserShow}
                                style={{ marginRight: "10px" }}
                                variant="contained"
                                color="secondary"
                                className='mu-button'
                                startIcon={<DeleteIcon />}
                            >
                                Удалить
                            </Button>
                        </div>
                        :
                        <div className="btn-box">
                            <Button
                                style={{ marginRight: "10px", background: '#0079ca' }}
                                variant="contained"
                                color="primary"
                                className='mu-button'
                                startIcon={<InfoIcon />}
                            >
                                Инфо
                            </Button>
                            <Button
                                onClick={addUserShow}
                                variant="contained"
                                style={{ color: "white", background: "green", marginRight: "10px" }}
                                className='mu-button'
                                startIcon={<VisibilityIcon />}
                            >
                                Хочу посмотреть
                            </Button>
                        </div>

                    }

                </div>
                :
                <div className="actions">
                    <Button
                        variant="contained"
                        color="primary"
                        className='info-button'
                        startIcon={<InfoIcon />}
                    >
                        Инфо
                    </Button>
                </div>}




        </div>
    )
}

export default Card
