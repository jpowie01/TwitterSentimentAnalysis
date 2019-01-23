import * as React from 'react';
import {Panel} from 'react-bootstrap';
import './tweet-card.css';
import {WordAttentionPair} from './word-attention-pair';

export enum Sentiments {
    POSITIVE = "POSITIVE",
    NEUTRAL = "NEUTRAL",
    NEGATIVE = "NEGATIVE"
}

export class TweetCard extends React.Component<any, any> {
    public state: {
        created: string, fullname: string, nickname: string, photoUrl: string,
        textWithAttentions: WordAttentionPair[], textSentiment: Sentiments
    };

    constructor(props: {
        created: string, fullname: string, nickname: string, photoUrl: string,
        text: string, attentions: number[], sentiment: Sentiments
    }, context: any) {
        super(props, context);

        const preparedText: WordAttentionPair[] = this.prepareWordAttentionPairs(props.sentiment, props.text, props.attentions);

        this.state = {
            created: props.created,
            fullname: props.fullname,
            nickname: props.nickname,
            photoUrl: props.photoUrl,
            textSentiment: props.sentiment,
            textWithAttentions: preparedText,
        }; // intentional
    }

    public render() {

        return (
            <div className='TweetCard'>
                <Panel>
                    <Panel.Body>
                        <div className='TweetUserInfo'>
                            <img src={this.state.photoUrl}/>
                            <span className='UserFullName'>{this.state.fullname}</span>
                            <span className='UserFullNick'>{'@' + this.state.nickname}</span>
                            <span className='TweetCreated'>{this.state.created}</span>
                        </div>
                        <span>
                            {this.state.textWithAttentions.map((pair, i) => pair.render())}
                        </span>
                    </Panel.Body>
                </Panel>
            </div>
        );
    }

    private prepareWordAttentionPairs(sentiment: Sentiments, text: string, attentions: number[]): WordAttentionPair[] {
        const words: string[] = text.split(" ");
        const wordAttentionPairs: WordAttentionPair[] = [];

        words.forEach((value: string, index: number, array: string[]) => {
            wordAttentionPairs.push(new WordAttentionPair({
                attention: attentions[index],
                sentiment,
                word: value,
            }, this.context));
        });

        return wordAttentionPairs;
    }
}