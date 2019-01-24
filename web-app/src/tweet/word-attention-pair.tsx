import * as React from 'react';
import { ColourUtil } from 'src/utils/ColourUtil';
import { Sentiments } from "./tweet-card";

export class WordAttentionPair extends React.Component<any, any> {
    public state: { sentiment: Sentiments, word: string, attention: number };

    constructor(props: { sentiment: Sentiments, word: string, attention: number }, context: any) {
        super(props, context);

        this.state = props;
    }

    public render() {
        const wordBackground: string = ColourUtil.getColourForSentimentAndAttention(this.state.sentiment, this.state.attention);
        const textStyle = {
            backgroundColor: wordBackground,
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
