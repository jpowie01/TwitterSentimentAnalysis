import * as React from 'react';
import {Sentiments} from "./tweet-card";


function GetColour(sentiment: Sentiments) {
    switch (sentiment) {
        case Sentiments.POSITIVE:
            return '0,255,0';
        case Sentiments.NEUTRAL:
            return '0,0,255';
        case Sentiments.NEGATIVE:
            return '255,0,0';
        default:
            return '255,255,0'
    }
}

export class WordAttentionPair extends React.Component<any, any> {
    public state: { sentiment: Sentiments, word: string, attention: number };

    constructor(props: { sentiment: Sentiments, word: string, attention: number }, context: any) {
        super(props, context);

        this.state = props;
    }

    public render() {
        const textStyle = {
            backgroundColor: 'rgba(' + GetColour(this.state.sentiment) + ',' + this.state.attention + ')',
            display: 'inline-block'
        };
        const spanStyle = {
            display: 'inline-block'
        };
        return (
            <span style={spanStyle}>
                &nbsp;<p style={textStyle}>{this.state.word}</p>
            </span>
        )
    }
}
