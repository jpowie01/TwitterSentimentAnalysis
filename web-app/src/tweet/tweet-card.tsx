import * as React from 'react';
import { Panel } from 'react-bootstrap';
import './tweet-card.css';
import { WordAttentionPair } from './word-attention-pair';

export enum Sentiments {
    POSITIVE = "POSITIVE",
    NEUTRAL = "NEUTRAL",
    NEGATIVE = "NEGATIVE",
    NONE = "NONE"
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

        const preparedText: WordAttentionPair[] = WordAttentionPair.prepareWordAttentionPairs(props.sentiment, props.text, props.attentions, this.context);

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
                        <span className='TweetPredictedSentiment'>{this.state.textSentiment}</span>
                        <div className='TweetUserInfo'>
                            <img src={this.state.photoUrl} />
                            <div className='TweetUsernames'>
                                <span className='UserFullName'>{this.state.fullname}</span>
                                <span className='UserFullNick'>{'@' + this.state.nickname}</span>
                            </div>
                        </div>
                        <span className='TweetText'>
                            {this.state.textWithAttentions.map((pair, i) => pair.render())}
                        </span>
                        <span className='TweetCreated'>{this.state.created}</span>
                    </Panel.Body>
                </Panel>
            </div>
        );
    }
}