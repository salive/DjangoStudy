import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => (
    <div>
        <h1 style={{ color: 'white' }}>Упс, такой страницы не существует</h1>
        <Link style={{ color: 'white' }} to="/">На главную</Link>
    </div>
);

export default NotFound;