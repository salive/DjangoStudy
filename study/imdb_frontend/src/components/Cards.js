import Card from "./Card"
import React from 'react'


const Cards = ({ shows, setShows, userShows, setUserShows }) => {
    return (
        <div className="cards">
            {shows.map((show) => (<Card
                userShows={userShows}
                setUserShows={setUserShows}
                shows={shows} key={show.id}
                id={show.id}
                year={show.year}
                title={show.title}
                poster={show.img_web ? show.poster : 'http://localhost:8000' + show.poster}
                rating={show.rating}
                description={show.description}
                is_series={show.is_series}
                setShows={setShows}
            />))}
        </div>
    )
}

export default Cards
