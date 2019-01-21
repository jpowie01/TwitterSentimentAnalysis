import * as React from 'react';

export class WordAttentionPair extends React.Component<any, any> {
    public state: {word: string, attention: number};

    constructor(props: { word: string, attention: number}, context: any) {
        super(props, context);

        this.state = props;
    }

    public render() {
        const textStyle = {
            backgroundColor: 'rgba(255,255,0,' + this.state.attention + ')',
            display: 'inline-block'
        };
        const spanStyle = {
            display: 'inline-block'
        }
        return (
            <span style={spanStyle}>
                &nbsp;<p style={textStyle}>{this.state.word}</p>
            </span>
        )
    }
}
