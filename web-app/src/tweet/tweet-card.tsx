import * as React from 'react';
import { Panel } from 'react-bootstrap';
import './tweet-card.css';

export enum Sentiments {
    POSITIVE,
    NEGATIVE
}

export class TweetCard extends React.Component<any, any> {
    public state: { text: string, sentiment: Sentiments };

    constructor(props: { text: string, sentiment: Sentiments }, context: any) {
        super(props, context);

        this.state = props; // intentional
    }

    public render() {
        return (
            <div className='TweetCard'>
                <Panel bsStyle="primary">
                    <Panel.Heading>
                        <Panel.Title componentClass="h3">
                            Tweet
                    </Panel.Title>
                    </Panel.Heading>
                    <Panel.Body>
                        {this.state.text}
                    </Panel.Body>
                </Panel>
            </div>
        );
    }
}