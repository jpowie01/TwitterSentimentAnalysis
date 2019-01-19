import * as React from 'react';
import { FormControl } from 'react-bootstrap';
import './search-form.css';

export class SearchForm extends React.Component {
    public state: { value: string };

    constructor(props: {}, context: any) {
        super(props, context);

        this.onChange = this.onChange.bind(this);

        this.state = {
            value: ''
        }
    }

    public render() {
        return (
            <div className='SearchForm'>
                <form className='SearchForm-input'>
                    <FormControl
                        type="text"
                        value={this.state.value}
                        placeholder="Enter phrase, username or hashtag"
                        onChange={this.onChange}
                        onBlur={this.onBlur} />
                </form>
            </div>
        );
    }

    private onBlur(): void {
        // alert('Blur');
    }

    private onChange(event: React.FormEvent<FormControl>): void {
        const element = event.target as HTMLInputElement;
        this.setState({
            value: element.value
        });
    }
}